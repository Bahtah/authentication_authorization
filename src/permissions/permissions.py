from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from permissions.models import UserRole

def admin_only(view_func):
    @wraps(view_func)
    def _wrapped(self, request, *args, **kwargs):
        user = getattr(request, "user", None)
        if not user:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        is_admin = UserRole.objects.filter(user=user, role__name="admin").exists()
        if not is_admin:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        return view_func(self, request, *args, **kwargs)
    return _wrapped

def admin_or_read_only(view_func):
    def wrapper(self, request, *args, **kwargs):
        user = request.user

        if request.method in ("GET", "HEAD", "OPTIONS"):
            return view_func(self, request, *args, **kwargs)

        is_admin = UserRole.objects.filter(user=user, role__name="admin").exists()

        if not (user and is_admin):
            return Response(
                {"error": "Admin privileges required."},
                status=status.HTTP_403_FORBIDDEN
            )

        return view_func(self, request, *args, **kwargs)
    return wrapper


def read_only(view_func):
    def wrapper(self, request, *args, **kwargs):
        if request.method not in ("GET", "HEAD", "OPTIONS"):
            return Response(
                {"error": "This endpoint is read-only."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return view_func(self, request, *args, **kwargs)
    return wrapper
