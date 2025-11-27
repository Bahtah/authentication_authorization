from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from permissions.utils import admin_required
from users.utils import token_required

REPORTS = [
    {"id": 1, "title": "Report 1"},
    {"id": 2, "title": "Report 2"},
    {"id": 3, "title": "Report 3"},
]

class ReportsAdminAPIView(APIView):
    @token_required
    @admin_required
    def get(self, request):
        return Response(REPORTS, status=status.HTTP_200_OK)

class ReportAllAPIView(APIView):
    @token_required
    def get(self, request):
        return Response(REPORTS, status=status.HTTP_200_OK)
