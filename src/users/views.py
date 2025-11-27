from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import SessionToken
from users.serializers import RegistrationSerializer, LoginSerializer, UpdateUserSerializer
from users.utils import token_required


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "middle_name": user.middle_name,
                "email": user.email,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            session_token = serializer.validated_data["session_token"]
            return Response(
                {"token": session_token},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeAPIView(APIView):

    @token_required
    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "middle_name": user.middle_name,
            "email": user.email
        }, status=status.HTTP_200_OK)

class MeUpdateAPIView(APIView):

    @token_required
    def patch(self, request):
        serializer = UpdateUserSerializer(instance=request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):

    @token_required
    def post(self, request):
        request.session_token.delete()
        return Response({"detail": "Logged out"}, status=status.HTTP_200_OK)

class MeDeleteAPIView(APIView):

    @token_required
    def delete(self, request):
        if not request.user.is_active:
            return Response({"detail": "User is already deleted"}, status=status.HTTP_401_UNAUTHORIZED)

        request.user.is_active = False
        request.user.save()

        SessionToken.objects.filter(user=request.user).delete()

        return Response({"detail": "User deleted"}, status=status.HTTP_200_OK)