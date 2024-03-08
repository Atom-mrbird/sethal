from django.urls import path, include
from .views import ShopView, addressview
from user.views import signup_view, verify_email,verify_email_done ,verify_email_complete,verify_email_confirm


urlpatterns = [
    path("shop/", ShopView, name="shop"),
    path("address/", addressview, name="address"),
    path("user/", include("user.urls")),
]