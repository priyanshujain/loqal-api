"""
List of plaid plugins exceptions
"""


class PlaidReAuth(Exception):
    pass


class PlaidBankUsernameExpired(Exception):
    pass


class PlaidFailed(Exception):
    pass
