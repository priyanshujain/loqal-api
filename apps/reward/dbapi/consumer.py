from apps.reward.models import LoyaltyProgram


def get_all_loyalty_programs():
    return LoyaltyProgram.objects.filter(is_active=True)