from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from shoppingcart.serializers import ProductSerializer
from shoppingcart.models import Product
from django.shortcuts import redirect
from shoppingcart.services import Cart
from django.shortcuts import render
from django.contrib import messages
class ProductAPI(APIView):
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

def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        quantity = request.POST['quantity']
        cart_item, created = Cart.objects.get_or_create(product=product, user=request.user)
        cart_item.quantity += int(quantity)
        cart_item.save()
        messages.success(request, f"{quantity} {product.name}(s) added to your cart.")
        return redirect('shop')
    return redirect('shop')


def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'registration/cartl.html', {'cart': cart_items})