from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=128)  # will store hashed password

    def __str__(self):
        return self.email

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.URLField()

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.first_name} - {self.product.name} ({self.quantity})"

    @property
    def total_price(self):
        return self.product.price * self.quantity
