# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils import six

# def get reset_token():
# 	def _make_hash_value(self, user, timestamp):
#         return (
#             six.text_type(user.pk) + six.text_type(timestamp) +
#             six.text_type(user.profile.email_confirmed)
#         )