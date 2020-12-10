import re

from django.db.utils import IntegrityError

from apps.merchant.models import AccountMember, FeatureAccessRole, MemberInvite
from apps.user.dbapi import create_user


def get_account_member_by_id(member_id, merchant_id):
    try:
        return AccountMember.objects.get(id=member_id, merchant_id=merchant_id)
    except AccountMember.DoesNotExist:
        return None


def create_account_member_on_reg(user_id, merchant_id, member_role_id):
    try:
        return AccountMember.objects.create(
            user_id=user_id,
            merchant_id=merchant_id,
            role_id=member_role_id,
            is_primary_member=True,
            account_active=True,
        )
    except IntegrityError:
        return None


def get_account_member_by_user_id(user_id):
    try:
        return AccountMember.objects.get(user_id=user_id)
    except AccountMember.DoesNotExist:
        return None


def create_feature_access_role(
    merchant_id,
    role_name,
    description,
    team_and_roles,
    beneficiaries,
    transactions,
    banking,
    settings,
    is_editable=True,
    is_standard_user=False,
    is_super_admin=False,
):
    try:
        return FeatureAccessRole.objects.create(
            merchant_id=merchant_id,
            role_name=role_name,
            description=description,
            team_and_roles=team_and_roles,
            beneficiaries=beneficiaries,
            transactions=transactions,
            banking=banking,
            settings=settings,
            is_editable=is_editable,
            is_standard_user=is_standard_user,
            is_super_admin=is_super_admin,
        )
    except IntegrityError:
        return None


def update_feature_access_role(
    role,
    description,
    team_and_roles,
    beneficiaries,
    transactions,
    banking,
    settings,
):
    role.description = description
    role.team_and_roles = team_and_roles
    role.beneficiaries = beneficiaries
    role.transactions = transactions
    role.banking = banking
    role.settings = settings
    role.save()
    return role


def get_standard_user_role(merchant_id):
    try:
        return FeatureAccessRole.objects.get(
            merchant_id=merchant_id, is_standard_user=True
        )
    except FeatureAccessRole.DoesNotExist:
        return None


def get_super_admin_role(merchant_id):
    try:
        return FeatureAccessRole.objects.get(
            merchant_id=merchant_id, is_super_admin=True
        )
    except FeatureAccessRole.DoesNotExist:
        return None


def add_account_access_to_profile(profile_id, merchant_id, role_id):
    member_qs = AccountMember.objects.filter(profile_id=profile_id)
    member_qs.update(merchant_id=merchant_id, role_id=role_id)
    return member_qs.first()


def remove_account_access_to_profile(profile_id, merchant_id, role_id):
    member_qs = AccountMember.objects.filter(profile_id=profile_id).update(
        merchant_id=None, role_id=None
    )
    return member_qs.first()


def get_primary_user(merchant_id):
    member_qs = AccountMember.objects.filter(
        merchant_id=merchant_id, is_primary_member=True
    )
    if not member_qs.exists():
        return None

    account_member = member_qs.first()
    return account_member.user


def get_account_invites(merchant_id):
    return MemberInvite.account_invites(merchant_id=merchant_id)


def create_member_invite(
    merchant_id, first_name, last_name, email, role_id, position
):
    invite = MemberInvite.objects.create(
        merchant_id=merchant_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        position=position,
        role_id=role_id,
    )
    invite.generate_invite_token()
    return invite


def get_member_invite_by_email(email):
    try:
        return MemberInvite.objects.get(email=email)
    except MemberInvite.DoesNotExist:
        return None


def get_member_invite_by_id(invite_id, merchant_id):
    try:
        return MemberInvite.objects.get(id=invite_id, merchant_id=merchant_id)
    except MemberInvite.DoesNotExist:
        return None


def get_feature_access_role_by_id(role_id, merchant_id):
    try:
        return FeatureAccessRole.objects.get(
            id=role_id, merchant_id=merchant_id
        )
    except FeatureAccessRole.DoesNotExist:
        return None


def get_feature_access_roles_by_account(merchant_id):
    return FeatureAccessRole.objects.filter(merchant_id=merchant_id)


def get_member_invite_by_token(token):
    try:
        return MemberInvite.objects.get(token__iexact=token)
    except MemberInvite.DoesNotExist:
        return None


def update_member_invite(
    invite, first_name, last_name, email, position, role_id
):
    invite.first_name = first_name
    invite.last_name = last_name
    invite.email = email
    invite.position = position
    invite.role_id = role_id
    invite.save()
    return invite


def create_account_member_from_team_invite(
    invite, first_name, last_name, phone_number, position, password
):
    user = create_user(
        first_name=first_name,
        last_name=last_name,
        email=invite.email,
        phone_number=phone_number,
        password=password,
        email_verified=True,
    )
    return AccountMember.objects.create(
        user_id=user.id,
        merchant_id=invite.account.id,
        role_id=invite.role.id,
        position=position,
        account_active=True,
    )


def get_members_by_account(merchant_id):
    return AccountMember.objects.filter(merchant_id=merchant_id)


def check_if_roles_exists_by_name(role_name, merchant_id):
    return FeatureAccessRole.objects.filter(
        role_name__iexact=role_name, merchant_id=merchant_id
    ).exists()


def check_members_exists_by_role(role_id, merchant_id):
    return AccountMember.objects.filter(
        role_id=role_id, merchant_id=merchant_id
    ).exists()


def check_invites_exists_by_role(role_id, merchant_id):
    return MemberInvite.objects.filter(
        role_id=role_id, merchant_id=merchant_id
    ).exists()
