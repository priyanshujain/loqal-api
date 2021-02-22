from apps.merchant.options import AllowedFeatureAcessTypes

__all__ = "DEFAULT_ROLE"

DEFAULT_ROLE = {
    "payment_requests": AllowedFeatureAcessTypes.PAYMENT_REQUESTS,
    "payment_history": AllowedFeatureAcessTypes.PAYMENT_HISTORY,
    "settlements": AllowedFeatureAcessTypes.SETTLEMENTS,
    "refunds": AllowedFeatureAcessTypes.REFUNDS,
    "disputes": AllowedFeatureAcessTypes.DISPUTES,
    "customers": AllowedFeatureAcessTypes.CUSTOMERS,
    "bank_accounts": AllowedFeatureAcessTypes.BANK_ACCOUNTS,
    "qr_codes": AllowedFeatureAcessTypes.QR_CODES,
    "store_profile": AllowedFeatureAcessTypes.STORE_PROFILE,
    "team_management": AllowedFeatureAcessTypes.TEAM_MANAGEMENT,
}
