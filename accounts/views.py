from django.shortcuts import render, redirect
from .forms import AddressForm
from shoppingcart.models import Product
def ShopView(request):
    products = Product.objects.all()
    return render(request, 'shop.html',context={
        "products":products
    })
def AboutView(request):
    return render(request, 'team.html')
def ContactView(request):
    return render(request, 'contact.html')
def addressview(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AddressForm()
    return render(request, 'client.html', {'form': form})