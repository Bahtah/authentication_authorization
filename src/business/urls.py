from django.urls import path

from business.views import ReportsAdminAPIView, ReportAdminOrReadOnlyAPIView, ReportUserAPIView

urlpatterns = [
    path('reports/admin/', ReportsAdminAPIView.as_view(), name='reports'),
    path('reports/admin-or-readonly/', ReportAdminOrReadOnlyAPIView.as_view(), name='reports-admin-or-readonly'),
    path('reports/user/', ReportUserAPIView.as_view(), name='reports-user')
]