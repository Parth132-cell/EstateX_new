from dataclasses import dataclass
from decimal import Decimal

from django.utils import timezone

from .models import NegotiationHistory, PropertyListing


@dataclass
class NegotiationSuggestion:
    suggested_counter: Decimal
    rationale: str


def suggest_counter_offer(listing: PropertyListing, proposed_amount: Decimal) -> NegotiationSuggestion:
    listing_age_days = max((timezone.now() - listing.created_at).days, 1)
    market_anchor = listing.price

    history = list(listing.negotiations.order_by('-timestamp')[:10])
    previous_amounts = [entry.amount for entry in history]
    average_previous = sum(previous_amounts) / len(previous_amounts) if previous_amounts else market_anchor

    age_discount = Decimal(min(listing_age_days, 90)) / Decimal('1000')
    target_ratio = Decimal('0.98') - age_discount
    floor_ratio = Decimal('0.88')

    target_price = max(market_anchor * max(target_ratio, floor_ratio), average_previous * Decimal('0.97'))
    suggested = max(target_price, proposed_amount * Decimal('1.02'))
    suggested = suggested.quantize(Decimal('0.01'))

    rationale = (
        f'Anchored to listing market price {market_anchor} with age-adjusted ratio {max(target_ratio, floor_ratio):.3f} '
        f'and negotiation trend average {average_previous.quantize(Decimal("0.01"))}.'
    )
    return NegotiationSuggestion(suggested_counter=suggested, rationale=rationale)


def create_negotiation_entry(
    *,
    listing: PropertyListing,
    from_user: int,
    to_user: int,
    amount: Decimal,
    message: str,
    offer_type: str,
) -> NegotiationHistory:
    return NegotiationHistory.objects.create(
        listing=listing,
        from_user=from_user,
        to_user=to_user,
        amount=amount,
        message=message,
        offer_type=offer_type,
    )
