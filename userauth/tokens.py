"""
this file is used to provide the account activation
 token in order for the user to activate their accounts through their email"""
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)
        )

account_activation_token = AccountActivationTokenGenerator()
