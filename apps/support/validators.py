from api import serializers


class SupportTicketValidator(serializers.ValidationSerializer):
    message = serializers.CharField(max_length=4 * 1024)
