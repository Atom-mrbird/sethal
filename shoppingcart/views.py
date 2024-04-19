from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from shoppingcart.serializers import ProductSerializer
from shoppingcart.models import Product
from django.shortcuts import redirect

from shoppingcart.services import Cart
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class ProductAPI(APIView):
    """
    Single API to handle product operations
    """
    serializer_class = ProductSerializer

    def get(self, request, format=None):
        qs = Product.objects.all()

        return Response(
            {"data": self.serializer_class(qs, many=True).data},
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class CartAPI(APIView):
    """
    Single API to handle cart operations
    """

    def get(self, request, format=None):
        cart = Cart(request)

        return Response(
            {"data": list(cart.__iter__()),
             "cart_total_price": cart.get_total_price()},
            status=status.HTTP_200_OK
        )

    def post(self, request, **kwargs):
        cart = Cart(request)

        if "remove" in request.data:
            product = request.data["product"]
            cart.remove(product)

        elif "clear" in request.data:
            cart.clear()

        else:
            product = request.data
            cart.add(
                product=product["product"],
                quantity=product["quantity"],
                overide_quantity=product["overide_quantity"] if "overide_quantity" in product else False
            )

        return Response(
            {"message": "cart updated"},
            status=status.HTTP_202_ACCEPTED)

"""@login_required
def add_to_cart(request, product_id):
    cart_item = Cart.objects.filter(user=request.user, product=product_id).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, "Item added to your cart.")
    else:
        Cart.objects.create(user=request.user, product=product_id)
        messages.success(request, "Item added to your cart.")

    return redirect("shoppingcart:cart_detail")

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id)

    if cart_item.user == request.user:
        cart_item.delete()
        messages.success(request, "Item removed from your cart.")

    return redirect("shoppingcart:cart_detail")

@login_required
def cart_detail(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = Cart(item.quantity * item.product.price for item in cart_items)
    context = {
        "cart_items": cart_items,
        "total_price": total_price,
    }

    return render(request, "registration/cart_detail.html", context)

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        messages.success(request, f"{product.name} added to your cart.")
        return redirect("shoppingcart:add_to_cart", product_id=product.id)

    context = {
        "product": product,
    }

    return render(request, "shop.html", context)"""
