from django.template.context_processors import static
from django.urls import path

from sethal import settings
from . import views
from shoppingcart.views import CartAPI, ProductAPI

app_name = "shoppingcart"

urlpatterns = [
    path('products/', ProductAPI.as_view(), name='products'),
    path('cart/', CartAPI.as_view(), name='cart'),
]