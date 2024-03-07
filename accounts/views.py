from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm, AddressForm

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignupForm()

    context = {'form': form}
    return render(request, 'registration/signup.html', context)

def ShopView(request):
    return render(request, 'shop.html')
def addressview(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AddressForm()
    return render(request, 'client.html', {'form': form})