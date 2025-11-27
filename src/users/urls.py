from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, MeAPIView, LogoutAPIView, MeUpdateAPIView, MeDeleteAPIView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('me/', MeAPIView.as_view(), name='me'),
    path('update/', MeUpdateAPIView.as_view(), name='update'),
    path('delete/', MeDeleteAPIView.as_view(), name='delete')
]
