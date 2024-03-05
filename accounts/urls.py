from django.urls import path
from .views import signup, ShopView


urlpatterns = [
    path("signup/", signup, name="signup"),
    path("shop/", ShopView, name="shop"),
]