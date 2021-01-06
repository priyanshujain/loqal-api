"""payment provider admin APIs"""


from django.db.utils import IntegrityError

from api.views import StaffAPIView, validate_serializer
from apps.provider.models import (PaymentProvider, PaymentProviderCred,
                                  TermsDocument)
from apps.provider.serializers import (ActivateTermDocumentSerializer,
                                       CreatePaymentProviderSerializer,
                                       CreateTermsDocumentSerializer,
                                       PaymentProviderCredSerializer,
                                       ProviderLogoUploadForm,
                                       RemoveTermDocumentSerializer,
                                       TermsDocumentSerializer,
                                       UpdatePaymentProviderSerializer)
from apps.provider.services import CreateProviderWebhook
from apps.provider.shortcuts import validate_image_data


class CreatePaymentProviderAPI(StaffAPIView):
    """Create new payment provider"""

    @validate_serializer(CreatePaymentProviderSerializer)
    def post(self, request):
        """Create new paymentprovider object"""
        data = request.data
        try:
            payment_provider = PaymentProvider.objects.create(**data)
        except IntegrityError:
            return self.error("PROVIDER_ALREADY_EXIST")

        return self.response(dict(id=payment_provider.id))


class UpdatePaymentProviderAPI(StaffAPIView):
    """Update new payment provider"""

    @validate_serializer(UpdatePaymentProviderSerializer)
    def put(self, request):
        """update paymentprovider object"""
        data = request.data
        payment_provider_qs = PaymentProvider.objects.filter(
            id=data["paymentprovider_id"]
        )
        if not payment_provider_qs.exists():
            return self.error("PROVIDER_DOES_NOT_EXIST")

        del data["paymentprovider_id"]
        payment_provider_qs.update(**data)

        return self.response()


class ProviderLogoUploadAPI(StaffAPIView):
    """Upload new/change logo"""

    request_parsers = ()

    def post(self, request):
        """upload/change logo"""
        form = ProviderLogoUploadForm(request.POST, request.FILES)
        if not form.is_valid():
            return self.error("INVALID_LOGO")

        data = form.cleaned_data
        if not validate_image_data(data["logo"]):
            return self.error("UNSUPPORTED_FILE_FORMAT")

        try:
            payment_provider = PaymentProvider.objects.get(
                id=data["paymentprovider_id"]
            )
        except PaymentProvider.DoesNotExist:
            return self.error("INVALID_PROVIDER")

        payment_provider.logo = data["logo"]
        payment_provider.save()
        return self.response()


class CreatePaymentProviderCredsAPI(StaffAPIView):
    """create payment provider creds"""

    @validate_serializer(PaymentProviderCredSerializer)
    def post(self, request):
        """Create payment provider creds object"""
        data = request.data
        provider_creds = PaymentProviderCred.objects.filter(
            provider_id=data["provider_id"],
            api_environment=data["api_environment"],
        )
        if provider_creds.exists():
            return self.error("CREDS_ALREADY_EXISTS")

        _ = PaymentProviderCred.objects.create(**data)
        return self.response()


class UpdatePaymentProviderCredsAPI(StaffAPIView):
    """Update payment provider creds"""

    @validate_serializer(PaymentProviderCredSerializer)
    def put(self, request):
        """update payment provider creds"""
        data = request.data
        PaymentProviderCred.objects.filter(
            provider_id=data["provider_id"]
        ).update(**data)
        return self.response()


class CreateTermDocumentAPI(StaffAPIView):
    """Upload new term document"""

    @validate_serializer(CreateTermsDocumentSerializer)
    def post(self, request):
        """Create a new terms documents"""
        data = request.data
        try:
            payment_provider = PaymentProvider.objects.get(
                id=data["provider_id"]
            )
        except PaymentProvider.DoesNotExist:
            return self.error("PAYMENT_PROVIDER_DOES_NOT_EXIST")

        # update old document to inactive
        TermsDocument.objects.filter(
            provider=payment_provider, country=data["country"]
        ).update(is_active=False)
        # Create new document
        _ = TermsDocument.objects.create(**data)

        return self.response()


class RemoveTermDocumentAPI(StaffAPIView):
    """Remove terms document if not being used"""

    @validate_serializer(RemoveTermDocumentSerializer)
    def post(self, request):
        """remove terms document object"""
        data = request.data

        try:
            terms_document = TermsDocument.objects.get(
                id=data["termdocument_id"]
            )
        except TermsDocument.DoesNotExist:
            return self.error("INVALID_TERM_DOCUMENT")

        termdocument_qs = TermsDocument.objects.filter(
            country=terms_document.country,
            document_type=terms_document.document_type,
            provider=terms_document.provider,
        )

        if termdocument_qs.count() < 2:
            return self.error("ADD_NEW_TO_REMOVE_OLD")

        return self.response()


class ActivateTermsDocumentAPI(StaffAPIView):
    """Activate terms document, automatically deactivates all other ones"""

    @validate_serializer(ActivateTermDocumentSerializer)
    def post(self, request):
        """Deactivate terms document"""
        data = request.data

        try:
            terms_document = TermsDocument.objects.get(
                id=data["termdocument_id"]
            )
        except TermsDocument.DoesNotExist:
            return self.error("INVALID_TERM_DOCUMENT")

        termdocument_qs = TermsDocument.objects.filter(
            country=terms_document.country,
            document_type=terms_document.document_type,
            provider=terms_document.provider,
        )
        termdocument_qs.update(is_active=False)
        terms_document.is_active = True
        terms_document.save()

        return self.response()


class ListTermsAPI(StaffAPIView):
    def get(self, request):
        payment_provider_slug = request.GET.get("payment_provider_slug", None)
        if not payment_provider_slug:
            return self.error("PROVIDER_SLUG_PARAMETER_NOT_FOUND")

        try:
            payment_provider = PaymentProvider.objects.get(
                provider_slug=payment_provider_slug
            )
        except PaymentProvider.DoesNotExist:
            return self.error("DOES_NOT_EXIST")

        terms_document_qs = TermsDocument.objects.filter(
            provider=payment_provider
        )
        if not terms_document_qs.exists():
            return self.error("NOT_FOUND")

        return self.response(
            TermsDocumentSerializer(terms_document_qs, many=True).data
        )


class CreateProviderWebhookAPI(StaffAPIView):
    """create webhook"""

    def post(self, request):
        CreateProviderWebhook().handle()
        return self.response()


# TODO: Provider Fee APIs
# 1. Local payment fees

# 2. Swift ours fee
# 3. Swift shared fees
#
# #########################
