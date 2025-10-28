from typing import Optional
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class UsernameOrEmailBackend(ModelBackend):
    def authenticate(self, request, username: Optional[str] = None, password: Optional[str] = None, **kwargs):
        User = get_user_model()
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        try:
            # Try username first
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Fallback to email
            try:
                user = User.objects.get(email__iexact=username)
            except User.DoesNotExist:
                return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None


