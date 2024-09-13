from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default='')

    def __str__(self):
        return self.name



# Create your models here.
class Dish(models.Model):
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(default='')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    url_img = models.URLField(blank=True)


    def __str__(self):
        return self.name


class Info(models.Model):
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=50)
    facebook = models.CharField(max_length=100)
    twitter = models.CharField(max_length=100)
    instagram = models.CharField(max_length=100)
    linkedin = models.CharField(max_length=100)
    pinterest = models.CharField(max_length=100)
