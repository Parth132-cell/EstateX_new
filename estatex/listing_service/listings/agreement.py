import uuid
from dataclasses import dataclass


@dataclass
class ESignDispatchResult:
    provider: str
    request_id: str


def generate_agreement_content(template_name: str, payload: dict) -> str:
    listing_title = payload.get('listing_title', 'Property')
    buyer_id = payload.get('buyer_id')
    seller_id = payload.get('seller_id')
    amount = payload.get('amount')
    return (
        f'Template: {template_name}\n'
        f'Listing: {listing_title}\n'
        f'Buyer ID: {buyer_id}\n'
        f'Seller ID: {seller_id}\n'
        f'Amount: {amount}\n'
        'Terms: Buyer and seller agree to execute sale as per escrow and due diligence conditions.'
    )


def send_to_esign_provider(provider: str, agreement_id: int) -> ESignDispatchResult:
    provider_name = provider or 'mock-esign'
    request_id = f'{provider_name}_{agreement_id}_{uuid.uuid4().hex[:10]}'
    return ESignDispatchResult(provider=provider_name, request_id=request_id)


def build_signed_pdf_url(agreement_id: int) -> str:
    return f'https://s3.amazonaws.com/estatex/agreements/{agreement_id}/signed.pdf'
