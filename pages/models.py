from django.db import models
from django.db.models.base import Model

# Create your models here.

#BestBuy table
class BestBuy(models.Model):
    SKU = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    Status = models.CharField(max_length=32)
    URL = models.CharField(max_length=256)
    Reviews = models.DecimalField(max_digits=3,decimal_places=2)

class User(models.Model):
    email = models.CharField(max_length=254,primary_key=True)
    password = models.CharField(max_length=256)

class products(models.Model):
    product = models.CharField(max_length=254,primary_key=True)
    MicroCenter_SKU = models.IntegerField()
    BestBuy_SKU = models.IntegerField()