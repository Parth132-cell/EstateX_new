import '../models/negotiation_entry.dart';
import '../models/property_listing.dart';
import '../network/api_client.dart';

class EstateXRepository {
  EstateXRepository({required ApiClient apiClient}) : _apiClient = apiClient;

  final ApiClient _apiClient;

  Future<List<PropertyListing>> fetchListings({String? city, int? maxPrice, int? bhk}) async {
    final rows = await _apiClient.getJsonList('/listings/', queryParameters: {
      if (city != null && city != 'All') 'city': city,
      if (maxPrice != null) 'max_price': maxPrice,
      if (bhk != null) 'bhk': bhk,
    });
    return rows.map((item) => PropertyListing.fromJson(item as Map<String, dynamic>)).toList();
  }

  Future<List<NegotiationEntry>> fetchOfferHistory(int listingId) async {
    final rows = await _apiClient.getJsonList('/offers/history/', queryParameters: {'listing_id': listingId});
    return rows.map((row) => NegotiationEntry.fromJson(row as Map<String, dynamic>)).toList();
  }

  Future<void> createOffer({required int listingId, required String fromUser, required String toUser, required int amount}) async {
    await _apiClient.postJson('/offers/', {
      'listing_id': listingId,
      'from_user': fromUser,
      'to_user': toUser,
      'amount': amount,
      'message': 'Offer from mobile app',
    });
  }

  Future<void> createCounter({required int listingId, required String fromUser, required String toUser, required int amount}) async {
    await _apiClient.postJson('/offers/counter/', {
      'listing_id': listingId,
      'from_user': fromUser,
      'to_user': toUser,
      'amount': amount,
      'message': 'Counter from mobile app',
    });
  }

  Future<void> createEscrowOrder({required int listingId, required int buyerId, required int sellerId, required int amount}) async {
    await _apiClient.postJson('/payments/create-order/', {
      'listing_id': listingId,
      'buyer_id': buyerId,
      'seller_id': sellerId,
      'amount': amount,
    });
  }

  Future<void> holdEscrow({required String providerReference}) async {
    await _apiClient.postJson('/payments/hold/', {'provider_reference': providerReference});
  }

  Future<void> releaseEscrow({required String providerReference}) async {
    await _apiClient.postJson('/payments/release/', {'provider_reference': providerReference});
  }

  Future<void> scheduleTour({required int listingId, required int hostId}) async {
    await _apiClient.postJson('/tours/schedule/', {
      'listing_id': listingId,
      'host_id': hostId,
      'scheduled_at': DateTime.now().add(const Duration(hours: 2)).toIso8601String(),
      'recording_enabled': false,
    });
  }
}
