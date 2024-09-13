from django.db import models
from user.models import Customer
from home.models import Dish

# Create your models here.

class Cart(models.Model):
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)


class CartItems(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    dish_id = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

