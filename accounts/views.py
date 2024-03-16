from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import AddressForm
from user.forms import UserRegisterForm


def ShopView(request):
    return render(request, 'shop.html')
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