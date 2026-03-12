from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal

from django.utils import timezone


FACE_MATCH_THRESHOLD = Decimal('0.750')
FRAUD_THRESHOLD = Decimal('0.700')
MAX_MEDIA_AGE_DAYS = 180


@dataclass
class VerificationEvaluation:
    gps_metadata_present: bool
    timestamp_valid: bool
    ai_fraud_score: Decimal
    passed: bool


def run_ai_fraud_detection(payload: dict) -> Decimal:
    """
    Placeholder for AI fraud microservice call.
    Returns deterministic score in [0.0, 1.0] to keep API testable.
    """
    explicit_score = payload.get('ai_fraud_score')
    if explicit_score is not None:
        return Decimal(str(explicit_score))

    suspicious_flags = payload.get('suspicious_flags', 0)
    base = Decimal('0.150') + (Decimal(str(suspicious_flags)) * Decimal('0.100'))
    return min(base, Decimal('1.000'))


def evaluate_verification(payload: dict) -> VerificationEvaluation:
    metadata = payload.get('image_metadata', {})
    gps_metadata_present = bool(metadata.get('geo_lat') is not None and metadata.get('geo_lng') is not None)

    media_timestamp = payload.get('media_timestamp')
    timestamp_valid = False
    if media_timestamp:
        max_age = timezone.now() - timedelta(days=MAX_MEDIA_AGE_DAYS)
        timestamp_valid = media_timestamp >= max_age

    ai_score = run_ai_fraud_detection(payload)
    face_match_score = Decimal(str(payload.get('face_match_score', '0')))

    passed = (
        gps_metadata_present
        and timestamp_valid
        and face_match_score >= FACE_MATCH_THRESHOLD
        and ai_score <= FRAUD_THRESHOLD
    )

    return VerificationEvaluation(
        gps_metadata_present=gps_metadata_present,
        timestamp_valid=timestamp_valid,
        ai_fraud_score=ai_score,
        passed=passed,
    )
