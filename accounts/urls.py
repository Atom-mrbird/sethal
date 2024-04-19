from django.urls import path, include
from .views import ShopView, addressview,AboutView, ContactView


urlpatterns = [
    path("shop/", ShopView, name="shop"),
    path("about/", AboutView, name="about"),
    path("contact/", ContactView, name="contact"),
    path("address/", addressview, name="address"),
    path("user/", include("user.urls")),
    path("shoppingcart/", include("shoppingcart.urls")),
]