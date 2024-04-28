from django.template.context_processors import static
from django.urls import path

from sethal import settings
from . import views
from shoppingcart.views import ProductAPI, CartAPI

app_name = "shoppingcart"

urlpatterns = [
    path("products/", ProductAPI.as_view(), name="product_list"),
    path("cart/", CartAPI.as_view(), name="product_list"),
]