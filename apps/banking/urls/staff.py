from django.urls import path

from apps.banking.views.staff import SyncBankAccountAPI

urlpatterns = [
    path(
        "staff/<int:account_id>/accounts/sync/",
        SyncBankAccountAPI.as_view(),
        name="staff_sync_bank_accounts",
    ),
]
