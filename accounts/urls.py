from django.urls import path
from .views import signup, ShopView, addressview


urlpatterns = [
    path("signup/", signup, name="signup"),
    path("shop/", ShopView, name="shop"),
    path("address/", addressview, name="address"),
]