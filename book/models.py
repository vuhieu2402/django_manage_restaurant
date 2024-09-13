from django.db import models
from user.models import Customer

# Create your models here.

class TableReservations(models.Model):
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    table_number = models.IntegerField(null=True, blank=True)
    reservation_date = models.DateField(null=False, blank=False)
    time = models.TimeField(null=False, blank=False)

