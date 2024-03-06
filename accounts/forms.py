from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Address

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=120, help_text='Required. Enter a valid email address.')
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'birth_date', 'password1', 'password2')
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=120, help_text='Required. Enter a valid email address.', widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name','address', 'city', 'state', 'zip_code']