from .models import Address
from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=120, help_text='Required. Enter a valid email address.', widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address', 'city', 'state', 'zip_code', 'country', 'phone_number']
class ContactForm(forms.Form):
    name = forms.CharField(max_length=250)
    email = forms.EmailField()
    subject = forms.CharField(max_length=250)
    message = forms.CharField(widget=forms.Textarea)
