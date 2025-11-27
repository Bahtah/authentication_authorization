from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.utils import token_required
from .models import Role, Permission, RolePermission, UserRole
from .serializers import (
    RoleSerializer,
    PermissionSerializer,
    RolePermissionSerializer,
    UserRoleSerializer,
)
from .utils import admin_required


class RoleAdminAPIView(APIView):
    @token_required
    @admin_required
    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data["name"]

            if Role.objects.filter(name=name).exists():
                return Response(
                    {"detail": "Role with this name already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            role = serializer.save()
            return Response(RoleSerializer(role).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @token_required
    @admin_required
    def get(self, request):
        qs = Role.objects.all()
        serializer = RoleSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PermissionAdminAPIView(APIView):
    @token_required
    @admin_required
    def post(self, request):
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            perm = serializer.save()
            return Response(PermissionSerializer(perm).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @token_required
    @admin_required
    def get(self, request):
        qs = Permission.objects.all()
        serializer = PermissionSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RolePermissionAdminAPIView(APIView):
    @token_required
    @admin_required
    def post(self, request):
        serializer = RolePermissionSerializer(data=request.data)

        if serializer.is_valid():
            role = serializer.validated_data["role"]
            permission = serializer.validated_data["permission"]

            if RolePermission.objects.filter(role=role, permission=permission).exists():
                return Response(
                    {"detail": "This permission is already assigned to this role"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            rp = serializer.save()
            return Response(RolePermissionSerializer(rp).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @token_required
    @admin_required
    def get(self, request):
        qs = RolePermission.objects.select_related("role", "permission").all()
        serializer = RolePermissionSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRoleAdminAPIView(APIView):
    @token_required
    @admin_required
    def post(self, request):
        serializer = UserRoleSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            role = serializer.validated_data["role"]

            if UserRole.objects.filter(user=user, role=role).exists():
                return Response(
                    {"detail": "This role is already assigned to the user"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            ur = serializer.save()
            return Response({
                "id": ur.id,
                "user": str(ur.user.pk),
                "role": ur.role.id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @token_required
    @admin_required
    def delete(self, request):
        user_id = request.data.get("user")
        role_id = request.data.get("role")

        if not user_id or not role_id:
            return Response({"detail": "user and role required"}, status=status.HTTP_400_BAD_REQUEST)

        qs = UserRole.objects.filter(user__pk=user_id, role__pk=role_id)
        if not qs.exists():
            return Response({"detail": "UserRole not found"}, status=status.HTTP_404_NOT_FOUND)

        count, _ = qs.delete()

        return Response({"deleted": count}, status=status.HTTP_204_NO_CONTENT)

    @token_required
    @admin_required
    def get(self, request):
        qs = UserRole.objects.select_related("user", "role").all()
        data = [
            {"id": ur.id, "user": str(ur.user.pk), "role": ur.role.name}
            for ur in qs
        ]
        return Response(data, status=status.HTTP_200_OK)
