from django.contrib import admin
from accounts.models import Contact
# Register your models here.
from .models import Profile
from .models import Address
admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(Contact)