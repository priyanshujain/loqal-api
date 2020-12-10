__all__ = "DEFAULT_ROLES"

DEFAULT_ROLES = [
    {
        "role_name": "View Only",
        "description": "Can view all account data including beneficiaries and payments.",
        "team_and_roles": [
            "VIEW",
        ],
        "beneficiaries": [
            "VIEW",
        ],
        "transactions": [
            "VIEW",
        ],
        "banking": [
            "VIEW",
        ],
        "settings": ["CREATE", "UPDATE", "VIEW", "APPROVE", "DELETE"],
    },
    {
        "role_name": "Approver Only",
        "description": "All features from view only + Can approve payments and beneficiaries.",
        "team_and_roles": [
            "VIEW",
        ],
        "beneficiaries": [
            "VIEW",
            "APPROVE",
        ],
        "transactions": [
            "VIEW",
            "APPROVE",
        ],
        "banking": [
            "VIEW",
            "APPROVE",
        ],
        "settings": [
            "VIEW",
            "APPROVE",
        ],
    },
    {
        "role_name": "Creator Only",
        "description": "Can create and view all account data including beneficiaries and payments.",
        "team_and_roles": [
            "VIEW",
        ],
        "beneficiaries": [
            "CREATE",
            "UPDATE",
            "VIEW",
        ],
        "transactions": [
            "CREATE",
            "UPDATE",
            "VIEW",
        ],
        "banking": [
            "VIEW",
        ],
        "settings": [
            "VIEW",
        ],
    },
    {
        "role_name": "Standard User",
        "description": "Can do all operation except adding/ removing new members.",
        "team_and_roles": [
            "VIEW",
        ],
        "beneficiaries": [
            "CREATE",
            "UPDATE",
            "VIEW",
            "APPROVE",
            "DELETE",
        ],
        "transactions": [
            "CREATE",
            "UPDATE",
            "VIEW",
            "APPROVE",
        ],
        "banking": [
            "CREATE",
            "UPDATE",
            "VIEW",
        ],
        "settings": [
            "CREATE",
            "UPDATE",
            "VIEW",
        ],
        "is_editable": False,
        "is_standard_user": True,
    },
    {
        "role_name": "Account Admin",
        "description": "Can view all account data including beneficiaries and payments.",
        "team_and_roles": ["CREATE", "UPDATE", "VIEW", "DELETE"],
        "beneficiaries": [
            "CREATE",
            "UPDATE",
            "VIEW",
            "APPROVE",
            "DELETE",
        ],
        "transactions": [
            "CREATE",
            "UPDATE",
            "VIEW",
            "APPROVE",
        ],
        "banking": [
            "CREATE",
            "UPDATE",
            "VIEW",
        ],
        "settings": [
            "CREATE",
            "UPDATE",
            "VIEW",
        ],
        "is_super_admin": True,
        "is_editable": False,
    },
]
