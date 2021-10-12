from django.db import models
from django.db.models.base import Model

# Create your models here.

#BestBuy table
class BestBuy(models.Model):
    BestBuy_Name = models.CharField(max_length=256)
    BestBuy_price = models.DecimalField(max_digits=10,decimal_places=2)
    BestBuy_Status = models.CharField(max_length=32)
    BestBuy_Ratings = models.DecimalField(max_digits=3,decimal_places=2)
    BestBuy_Review = models.IntegerField()
    BestBuy_ModelNumber = models.CharField(max_length=128)
    BestBuy_SKU = models.IntegerField(primary_key=True)
    BestBuy_URL = models.CharField(max_length=256)

class MicroCenter(models.Model):
    MicroCenter_Name = models.CharField(max_length=256)
    MicroCenter_Price = models.DecimalField(max_digits=10,decimal_places=2)
    MicroCenter_SKU = models.IntegerField(primary_key=True)
    MicroCenter_ModelNumber = models.CharField(max_length=128)
    MicroCenter_URL = models.CharField(max_length=256)

class User(models.Model):
    email = models.CharField(max_length=254,primary_key=True)
    password = models.CharField(max_length=256)

class products(models.Model):
    product = models.CharField(max_length=254,primary_key=True)
    MicroCenter_SKU = models.IntegerField()
    BestBuy_SKU = models.IntegerField()