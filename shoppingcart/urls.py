from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from shoppingcart.views import add_to_cart, view_cart,checkout, delete_from_cart

app_name = "shoppingcart"

urlpatterns = [
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('view-cart/', view_cart, name='view-cart'),
    path('checkout/', checkout, name='checkout'),
    path('delete_from_cart/<int:product_id>/', delete_from_cart, name='delete_from_cart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)