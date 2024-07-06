from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from shoppingcart.serializers import ProductSerializer
from django.shortcuts import redirect
from shoppingcart.services import cartData, guestOrder, Product
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
import json
import datetime
from accounts.models import Address
from shoppingcart.models import Cart

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
    if not request.user.is_authenticated:
        return redirect('login')
    cart_items = Cart.objects.filter(user=request.user)
    address = Address.objects.filter(user=request.user)
    return render(request, 'registration/cartl.html', {'cart_items': cart_items, 'address': address})
def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'registration/cartl.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'checkout.html', context)


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Cart.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = Cart.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

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