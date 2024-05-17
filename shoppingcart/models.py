from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from user.models import CustomUser
class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products_images/', blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)

    def get_absolute_url(self):
        return reverse("shop")

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Changed to ForeignKey
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product}"

    def get_total_price(self):
        return self.quantity * self.product.price