from django import forms
from .models import Address

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=120, help_text='Required. Enter a valid email address.', widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name','address', 'city', 'state', 'zip_code']