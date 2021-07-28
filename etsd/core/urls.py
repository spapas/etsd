from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView

urlpatterns = [
    path(r"", TemplateView.as_view(template_name="home.html"), name="home"),
    path(r"login/", LoginView.as_view(), name="auth_login"),
    path(r"logout/", LogoutView.as_view(template_name="logout.html"), name="auth_logout"),
]
