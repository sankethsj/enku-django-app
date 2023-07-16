from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    # private routes
    path("property/", views.property_listing, name="property_listing"),
    path("property/add", views.upload_property, name="upload_property"),
    path("property/approve", views.property_approvals, name="property_approvals"),
    path("property/approve/<int:property_id>", views.property_approvals, name="property_approvals"),
    path("profile/listing", views.my_listing, name="my_listing"),
    path("profile/listing/delete/<int:property_id>", views.delete_my_listing, name="delete_my_listing")
]