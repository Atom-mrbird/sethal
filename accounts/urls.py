from django.urls import path
from .views import SignUpView, ShopView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("shop/", ShopView, name="shop"),
]