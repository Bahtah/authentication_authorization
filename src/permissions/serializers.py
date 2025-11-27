from rest_framework import serializers
from .models import Role, Permission, RolePermission, UserRole
from users.models import User


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name", "description", "created_at", "updated_at"]


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "name", "codename", "description", "created_at", "updated_at"]


class RolePermissionSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    permission = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all())

    class Meta:
        model = RolePermission
        fields = ["id", "role", "permission", "created_at", "updated_at"]


class UserRoleSerializer(serializers.ModelSerializer):
    user = serializers.UUIDField()
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model = UserRole
        fields = ["id", "user", "role", "created_at", "updated_at"]

    def validate_user(self, value):
        try:
            user = User.objects.get(pk=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")
        return user

    def create(self, validated_data):
        user = validated_data["user"]
        role = validated_data["role"]
        return UserRole.objects.create(user=user, role=role)
