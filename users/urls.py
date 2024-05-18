""""
URLs for users
"""


from django.urls import path

from users import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

app_name = 'users'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
