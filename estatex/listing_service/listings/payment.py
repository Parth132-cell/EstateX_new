import uuid
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class EscrowOrderResult:
    provider_order_id: str
    provider_reference: str
    amount: Decimal


def create_escrow_order(amount: Decimal, listing_id: int, buyer_id: int, seller_id: int) -> EscrowOrderResult:
    seed = uuid.uuid4().hex[:12]
    return EscrowOrderResult(
        provider_order_id=f'rzp_order_{seed}',
        provider_reference=f'escrow_{listing_id}_{buyer_id}_{seller_id}_{uuid.uuid4().hex[:8]}',
        amount=amount,
    )


def hold_escrow_funds(provider_order_id: str, payment_id: str) -> bool:
    return bool(provider_order_id and payment_id)


def release_escrow_funds(provider_reference: str) -> bool:
    return bool(provider_reference)
