from apps.user.models import User

for user in User.objects.all():
    phone_number = user.phone_number
    if phone_number:
        user.phone_number = phone_number[-10:]
        user.save()
