from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import *

from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('profile/', ProfileUpdateView.as_view(), name="profile"),
    ]


