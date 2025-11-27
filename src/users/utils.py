import hashlib

from functools import wraps
from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response

from users.models import SessionToken


def hash_password(password: str) -> str:
    """Hash password"""
    return hashlib.sha256(password.encode()).hexdigest()

def token_required(view_func):
    @wraps(view_func)
    def wrapped_view(self, request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response({"detail": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)

        session = SessionToken.objects.filter(token=auth_header.split()[1]).first()
        if not session:
            return Response({"detail": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED)

        if session.expires_at < timezone.now():
            session.delete()
            return Response({"detail": "Token expired"}, status=status.HTTP_401_UNAUTHORIZED)

        request.user = session.user
        request.session_token = session

        return view_func(self, request, *args, **kwargs)
    return wrapped_view