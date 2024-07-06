from django.conf import settings
from django.template.context_processors import media
from django.urls import path, include
from accounts.views import ShopView, addressview,AboutView, ContactView
from django.conf.urls.static import static

urlpatterns = [
    path("shop/", ShopView, name="shop"),
    path("about/", AboutView, name="about"),
    path("contact/", ContactView, name="contact"),
    path("address/", addressview, name="address"),
    path("user/", include("user.urls")),
    path("shoppingcart/", include("shoppingcart.urls")),
    ] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)