from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect

import accounts
from accounts.models import Contact
from .forms import AddressForm
from shoppingcart.models import Product

def ShopView(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products':products})
def AboutView(request):
    return render(request, 'team.html')
def ContactView(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if not name or not email or not subject or not message:
            return HttpResponse("All fields are required.", status=400)

        try:
            Contact.objects.create(name=name, email=email, subject=subject, message=message)
            return redirect('/success/')
        except IntegrityError as e:
            return HttpResponse(f"Integrity Error: {e}", status=500)
    return render(request, 'contact.html')


@login_required
def addressview(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=True)
            address.user_id = request.user
            address.save()
            return redirect('shoppingcart:checkout')
    else:
        form = AddressForm()
    return render(request, 'client.html', {'form': form})