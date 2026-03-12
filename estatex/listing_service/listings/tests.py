from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import NegotiationHistory, PropertyListing, Transaction, VerificationRecord


class PropertyListingAPITests(APITestCase):
    def setUp(self):
        self.list_url = reverse('listings-list')
        self.payload = {
            'broker_id': 44,
            'title': 'Modern 3BHK Apartment',
            'address': '12 Green Residency',
            'city': 'Bengaluru',
            'price': '12500000.00',
            'bhk': 3,
            'description': 'Close to metro station',
            'amenities': ['gym', 'pool'],
            'media_urls': ['s3://estatex/listings/1/front.jpg'],
        }

    def test_create_listing(self):
        response = self.client.post(self.list_url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PropertyListing.objects.count(), 1)

    def test_list_filter_by_city_and_bhk(self):
        PropertyListing.objects.create(**self.payload)
        PropertyListing.objects.create(
            broker_id=55,
            title='Budget 2BHK',
            address='77 Lake View',
            city='Pune',
            price='7500000.00',
            bhk=2,
            description='Near IT park',
            amenities=['parking'],
            media_urls=[],
        )

        response = self.client.get(f'{self.list_url}?city=Bengaluru&bhk=3')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['city'], 'Bengaluru')

    def test_search_listing(self):
        PropertyListing.objects.create(**self.payload)

        response = self.client.get(f'{self.list_url}?search=metro')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_update_listing(self):
        listing = PropertyListing.objects.create(**self.payload)

        response = self.client.patch(
            reverse('listings-detail', kwargs={'pk': listing.id}),
            {'price': '13000000.00'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        listing.refresh_from_db()
        self.assertEqual(str(listing.price), '13000000.00')

    def test_delete_listing(self):
        listing = PropertyListing.objects.create(**self.payload)

        response = self.client.delete(reverse('listings-detail', kwargs={'pk': listing.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PropertyListing.objects.filter(id=listing.id).exists())

    def test_verify_listing_success_queues_admin_review(self):
        listing = PropertyListing.objects.create(**self.payload)

        response = self.client.post(
            reverse('listings-verify-listing', kwargs={'pk': listing.id}),
            {
                'image_metadata': {'geo_lat': '12.9012345', 'geo_lng': '77.5432109'},
                'media_timestamp': (timezone.now() - timedelta(days=5)).isoformat(),
                'face_match_score': '0.890',
                'suspicious_flags': 1,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], VerificationRecord.Result.PENDING_ADMIN)
        self.assertEqual(response.data['admin_review_status'], 'queued')
        self.assertEqual(VerificationRecord.objects.count(), 1)

    def test_verify_listing_failure_marks_rejected(self):
        listing = PropertyListing.objects.create(**self.payload)

        response = self.client.post(
            reverse('listings-verify-listing', kwargs={'pk': listing.id}),
            {
                'image_metadata': {'geo_lat': None, 'geo_lng': None},
                'media_timestamp': (timezone.now() - timedelta(days=365)).isoformat(),
                'face_match_score': '0.400',
                'ai_fraud_score': '0.950',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], VerificationRecord.Result.FAILED)
        self.assertEqual(response.data['admin_review_status'], 'not_queued')

        listing.refresh_from_db()
        self.assertEqual(listing.verification_status, PropertyListing.VerificationStatus.REJECTED)


    def test_advanced_search_filters_verified_and_query(self):
        verified_listing = PropertyListing.objects.create(
            **{**self.payload, 'verification_status': PropertyListing.VerificationStatus.VERIFIED}
        )
        PropertyListing.objects.create(
            broker_id=90,
            title='Pending listing hidden',
            address='Nope street',
            city='Bengaluru',
            price='12900000.00',
            bhk=3,
            description='Should not appear',
            amenities=[],
            media_urls=[],
            verification_status=PropertyListing.VerificationStatus.PENDING,
        )

        response = self.client.get(reverse('listings-advanced-search') + '?q=metro&city=Bengaluru&page_size=10')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertFalse(response.data['cache_hit'])
        self.assertEqual(response.data['results'][0]['id'], verified_listing.id)

    def test_advanced_search_uses_cache_on_repeat(self):
        PropertyListing.objects.create(
            **{**self.payload, 'verification_status': PropertyListing.VerificationStatus.VERIFIED}
        )

        url = reverse('listings-advanced-search') + '?q=metro&city=Bengaluru&page_size=10'
        first = self.client.get(url)
        second = self.client.get(url)

        self.assertEqual(first.status_code, status.HTTP_200_OK)
        self.assertEqual(second.status_code, status.HTTP_200_OK)
        self.assertFalse(first.data['cache_hit'])
        self.assertTrue(second.data['cache_hit'])


    def test_schedule_video_tour(self):
        listing = PropertyListing.objects.create(**self.payload)
        response = self.client.post(
            reverse('tour-schedule'),
            {
                'listing_id': listing.id,
                'host_id': 44,
                'scheduled_at': (timezone.now() + timedelta(hours=2)).isoformat(),
                'recording_enabled': True,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('room_id', response.data)
        self.assertEqual(response.data['listing_id'], listing.id)
        self.assertEqual(response.data['status'], 'scheduled')

    def test_join_video_tour_sets_live_status_when_time_reached(self):
        listing = PropertyListing.objects.create(**self.payload)
        create_response = self.client.post(
            reverse('tour-schedule'),
            {
                'listing_id': listing.id,
                'host_id': 44,
                'scheduled_at': (timezone.now() - timedelta(minutes=5)).isoformat(),
                'recording_enabled': False,
            },
            format='json',
        )
        room_id = create_response.data['room_id']

        join_response = self.client.get(reverse('tour-join', kwargs={'room_id': room_id}))
        self.assertEqual(join_response.status_code, status.HTTP_200_OK)
        self.assertEqual(join_response.data['room_id'], room_id)
        self.assertEqual(join_response.data['status'], 'live')
        self.assertEqual(join_response.data['signaling']['type'], 'socketio')


    def test_create_offer_returns_ai_suggestion(self):
        listing = PropertyListing.objects.create(**self.payload)

        response = self.client.post(
            reverse('offer-create'),
            {
                'listing_id': listing.id,
                'from_user': 501,
                'to_user': 44,
                'amount': '12000000.00',
                'message': 'Initial offer from buyer',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('ai_suggestion', response.data)
        self.assertEqual(NegotiationHistory.objects.count(), 1)
        self.assertEqual(NegotiationHistory.objects.first().offer_type, NegotiationHistory.OfferType.OFFER)

    def test_counter_offer_and_history(self):
        listing = PropertyListing.objects.create(**self.payload)
        offer_response = self.client.post(
            reverse('offer-create'),
            {
                'listing_id': listing.id,
                'from_user': 501,
                'to_user': 44,
                'amount': '11800000.00',
                'message': 'Offer',
            },
            format='json',
        )
        offer_id = offer_response.data['offer_id']

        counter_response = self.client.post(
            reverse('offer-counter'),
            {
                'listing_id': listing.id,
                'reference_offer_id': offer_id,
                'from_user': 44,
                'to_user': 501,
                'amount': '12350000.00',
                'message': 'Counter offer',
            },
            format='json',
        )
        self.assertEqual(counter_response.status_code, status.HTTP_201_CREATED)

        history_response = self.client.get(reverse('offer-history') + f'?listing_id={listing.id}')
        self.assertEqual(history_response.status_code, status.HTTP_200_OK)
        self.assertEqual(history_response.data['count'], 2)
        self.assertEqual(history_response.data['results'][0]['offer_type'], NegotiationHistory.OfferType.OFFER)
        self.assertEqual(history_response.data['results'][1]['offer_type'], NegotiationHistory.OfferType.COUNTER)


    def test_payment_escrow_flow(self):
        listing = PropertyListing.objects.create(**self.payload)

        create_order = self.client.post(
            reverse('payment-create-order'),
            {
                'buyer_id': 501,
                'seller_id': 44,
                'listing_id': listing.id,
                'amount': '12500000.00',
            },
            format='json',
        )
        self.assertEqual(create_order.status_code, status.HTTP_201_CREATED)
        provider_reference = create_order.data['provider_reference']

        hold = self.client.post(
            reverse('payment-hold'),
            {
                'provider_reference': provider_reference,
                'provider_payment_id': 'pay_123',
            },
            format='json',
        )
        self.assertEqual(hold.status_code, status.HTTP_200_OK)
        self.assertEqual(hold.data['status'], Transaction.Status.FUNDS_HELD)

        release = self.client.post(
            reverse('payment-release'),
            {
                'provider_reference': provider_reference,
            },
            format='json',
        )
        self.assertEqual(release.status_code, status.HTTP_200_OK)
        self.assertEqual(release.data['status'], Transaction.Status.RELEASED)


    def test_agreement_generate_send_get(self):
        listing = PropertyListing.objects.create(**self.payload)

        generate = self.client.post(
            reverse('agreement-generate'),
            {
                'listing_id': listing.id,
                'buyer_id': 501,
                'seller_id': 44,
                'amount': '12500000.00',
                'template_name': 'estatex-sale-template-v1',
            },
            format='json',
        )
        self.assertEqual(generate.status_code, status.HTTP_201_CREATED)
        agreement_id = generate.data['agreement_id']

        send = self.client.post(
            reverse('agreement-send'),
            {
                'agreement_id': agreement_id,
                'provider': 'mockesign',
            },
            format='json',
        )
        self.assertEqual(send.status_code, status.HTTP_200_OK)
        self.assertEqual(send.data['status'], 'sent')

        detail = self.client.get(reverse('agreement-detail', kwargs={'agreement_id': agreement_id}))
        self.assertEqual(detail.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.data['status'], 'signed')
        self.assertIn('signed.pdf', detail.data['signed_pdf_url'])
