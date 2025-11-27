from django.urls import path
from . import views

urlpatterns = [
    path("admin/role/", views.RoleAdminAPIView.as_view(), name="admin-role"),
    path("admin/permission/", views.PermissionAdminAPIView.as_view(), name="admin-permission"),
    path("admin/role-permission/", views.RolePermissionAdminAPIView.as_view(), name="admin-role-permission"),
    path("admin/user-role/", views.UserRoleAdminAPIView.as_view(), name="admin-user-role"),
]
