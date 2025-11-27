import uuid
from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from users.models import User, SessionToken
from users.utils import hash_password


class RegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    middle_name = serializers.CharField(max_length=50, allow_blank=True, required=False)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError('Passwords do not match')
        attrs.pop("password_confirmation")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        password_hash = hash_password(password)
        validated_data["password"] = password_hash
        user = User.objects.create(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("User not found")

        password_hash = hash_password(password)
        if password_hash != user.password:
            raise serializers.ValidationError("Invalid password")

        if not user.is_active:
            raise serializers.ValidationError("User is not active")

        token = uuid.uuid4().hex
        expires_at = timezone.now() + timedelta(days=1)
        session_token = SessionToken.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )

        attrs.pop("password")
        attrs["session_token"] = session_token.token
        return attrs

class UpdateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    middle_name = serializers.CharField(max_length=50, allow_blank=True, required=False)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def update(self, instance, validated_data):
        if validated_data.get("password"):
            instance.password = hash_password(validated_data["password"])

        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.middle_name = validated_data.get("middle_name", instance.middle_name)
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance
