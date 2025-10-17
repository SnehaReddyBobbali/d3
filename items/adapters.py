from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.exceptions import ValidationError


class KLHSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter to restrict Google authentication to @klh.edu.in emails only
    """
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a social provider,
        but before the login is actually processed.
        """
        email = sociallogin.account.extra_data.get('email', '').lower()
        
        # Check if email ends with @klh.edu.in
        if not email.endswith('@klh.edu.in'):
            raise ValidationError(
                'Only KLH students with @klh.edu.in email addresses are allowed to sign in.'
            )
