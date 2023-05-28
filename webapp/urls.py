from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    # private routes
    path("workspace/", views.workspace, name="workspace"),
    path("workspace/preferences", views.workspace_preference, name="workspace_preferences")
]