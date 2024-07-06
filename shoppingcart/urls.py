from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from shoppingcart.views import ProductAPI, add_to_cart, view_cart,checkout,cart

app_name = "shoppingcart"

urlpatterns = [
    path('products/', ProductAPI.as_view(), name="product_list"),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('view-cart/', view_cart, name='view-cart'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)