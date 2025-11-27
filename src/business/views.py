from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from permissions.permissions import admin_only, read_only, admin_or_read_only, manager
from users.utils import token_required

REPORTS = [
    {"id": 1, "title": "Report 1"},
    {"id": 2, "title": "Report 2"},
    {"id": 3, "title": "Report 3"},
]

class ReportsAdminAPIView(APIView):

    """Просмотр доступен пользователям с ролью админ"""

    @token_required
    @admin_only
    def get(self, request):
        return Response(REPORTS, status=status.HTTP_200_OK)

class ReportAdminOrReadOnlyAPIView(APIView):

    """Просмотр доступен всем, создание и удаление доступно пользователям с ролью админ"""

    @token_required
    @admin_or_read_only
    def get(self, request):
        return Response(REPORTS, status=status.HTTP_200_OK)

    @token_required
    @manager
    def post(self, request):
        new_report = request.data.get("report")
        if not new_report:
            return Response({"error": "report is required"}, status=400)

        REPORTS.append(new_report)
        return Response({"message": "Report created", "data": new_report}, status=201)

    @token_required
    @manager
    def delete(self, request):
        report_index = request.data.get("index")
        if report_index is None or report_index >= len(REPORTS):
            return Response({"error": "Invalid index"}, status=400)

        deleted = REPORTS.pop(report_index)
        return Response({"message": "Report deleted", "data": deleted}, status=200)

class ReportUserAPIView(APIView):

    """Просмотр доступен всем"""

    @token_required
    @read_only
    def get(self, request):
        return Response(REPORTS, status=status.HTTP_200_OK)
