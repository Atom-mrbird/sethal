from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import redirect
from django.shortcuts import render, HttpResponse
from accounts.forms import ContactForm
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
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Save the contact message to the database
            Contact.objects.create(name=name, email=email, subject=subject, message=message)

            # Redirect to a success page
            return redirect('index')
        else:
            return HttpResponse("Invalid reCAPTCHA. Please try again.", status=400)
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


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