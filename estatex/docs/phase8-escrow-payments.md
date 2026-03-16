# EstateX Phase 8 — Escrow Payments

## Architecture decisions
- Escrow lifecycle is implemented in `listing_service` for immediate integration with listing transactions.
- `Transaction` is the source of truth for escrow states and provider references.
- Provider interaction is abstracted in `listings/payment.py`, allowing Razorpay/Stripe SDK swap later.

## Data model
`Transaction`
- `buyer_id`
- `seller_id`
- `listing` FK
- `amount`
- `status` (`order_created`, `funds_held`, `released`, `failed`)
- `provider_reference`
- `provider_order_id`
- `provider_payment_id`
- `metadata`

## Endpoints
- `POST /payments/create-order`
  - creates escrow order and transaction row
- `POST /payments/hold`
  - marks funds held after provider payment confirmation
- `POST /payments/release`
  - releases funds to seller after agreement completion

## Escrow flow
1. Buyer creates order (`order_created`).
2. Provider confirms payment capture/hold (`funds_held`).
3. After agreement confirmation, platform releases (`released`).

## Tests
- End-to-end API test for create order -> hold -> release status transitions.
