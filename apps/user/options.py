from utils.choices import Choices


class UserType(Choices):
    REGULAR_USER = "REGULAR_USER"
    REGULAR_STAFF = "REGULAR_STAFF"
    ADMIN_STAFF = "ADMIN_STAFF"
