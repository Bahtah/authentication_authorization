from django.urls import path

from business.views import ReportsAdminAPIView, ReportAllAPIView

urlpatterns = [
    path('reports/', ReportsAdminAPIView.as_view(), name='business-reports'),
    path('reports/all/', ReportAllAPIView.as_view(), name='business-reports-all')
]