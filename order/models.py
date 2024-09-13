from django.db import models
from user.models import Customer
from home.models import Dish
# Create your models here.

class Order(models.Model):
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_price = models.DecimalField(decimal_places=2, max_digits=10)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)


class OrderDetails(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish_id = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)

    def total_price(self):
        return self.quantity * self.unit_price
