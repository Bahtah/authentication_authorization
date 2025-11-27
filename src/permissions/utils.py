from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .models import UserRole

def admin_required(view_func):
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
