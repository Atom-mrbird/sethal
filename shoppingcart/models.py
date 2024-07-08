from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from user.models import CustomUser

from django.core.files import File

from io import BytesIO
from PIL import Image

class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)

    def get_absolute_url(self):
        return reverse("shop")

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name

    def get_display_price(self):
        return self.price / 100

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x240x.jpg'

    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'jpg', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

    def __str__(self) -> str:
        return str(self.name)

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Changed to ForeignKey
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product}"

    def get_total_price(self):
        return self.quantity * self.product.price

class Order(models.Model):
        customer = models.ForeignKey('user.CustomUser', on_delete=models.SET_NULL, null=True, blank=True)
        date_ordered = models.DateTimeField(auto_now_add=True)
        complete = models.BooleanField(default=False)
        transaction_id = models.CharField(max_length=100, null=True)
        def __str__(self):
            return str(self.id)
@property
def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
@property
def get_cart_total(self):
    orderitems = self.orderitem_set.all()
    total = sum([item.get_total for item in orderitems])
    return total
@property
def get_cart_items(self):
    orderitems = self.orderitem_set.all()
    total = sum([item.quantity for item in orderitems])
    return total
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
@property
def get_total(self):
        total = self.product.price * self.quantity
        return total
