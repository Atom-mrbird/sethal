from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from shoppingcart.serializers import ProductSerializer
from django.shortcuts import redirect
from shoppingcart.services import guestOrder
from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from accounts.models import Address
from shoppingcart.models import Product, Cart

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)
        quantity = int(request.POST.get('quantity', 1))
        cart_item, created = Cart.objects.get_or_create(product=product, user=request.user)
        cart_item.quantity += quantity
        cart_item.save()

        # Get updated cart info
        cart_items = Cart.objects.filter(user=request.user)
        total_quantity = sum(item.quantity for item in cart_items)
        total_price = sum(item.quantity * item.product.price for item in cart_items)
        response_data = {
            'total_quantity': total_quantity,
            'total_price': total_price,
        }

        return JsonResponse(response_data)

    return redirect('shop')
def remove(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        cart_item = Cart.objects.filter(product=product, user=request.user).first()

        if cart_item:
            cart_item.delete()

        # Get updated cart info
        cart_items = Cart.objects.filter(user=request.user)
        total_quantity = sum(item.quantity for item in cart_items)
        total_price = sum(item.quantity * item.product.price for item in cart_items)
        response_data = {
            'total_quantity': total_quantity,
            'total_price': total_price,
        }

        return JsonResponse(response_data, status=200)

    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

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




def view_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.quantity * item.product.price for item in cart_items)
    address = Address.objects.filter(user=request.user).first()  # Assuming one address per user
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'address': address,
    }
    return render(request, 'registration/cartl.html', context)

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.quantity * item.product.price for item in cart_items)
    address = Address.objects.filter(user=request.user).first()
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'address': address,
    }
    return render(request, 'checkout.html', context)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Cart.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
	    Address.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)