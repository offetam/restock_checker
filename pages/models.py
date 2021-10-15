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
    BestBuy_UUID = models.CharField(max_length=128)

class MicroCenter(models.Model):
    MicroCenter_Name = models.CharField(max_length=256)
    MicroCenter_Price = models.DecimalField(max_digits=10,decimal_places=2)
    MicroCenter_SKU = models.IntegerField(primary_key=True)
    MicroCenter_ModelNumber = models.CharField(max_length=128)
    MicroCenter_URL = models.CharField(max_length=256)
    MicroCenter_UUID = models.CharField(max_length=128)

class Gamestop(models.Model):
    Gamestop_SKU = models.IntegerField(primary_key=True)
    Gamestop_Name = models.CharField(max_length=256)
    Gamestop_price = models.DecimalField(max_digits=10,decimal_places=2)
    Gamestop_URL = models.CharField(max_length=256)
    Gamestop_Status = models.CharField(max_length=32)
    Gamestop_UUID = models.CharField(max_length=128)

class BH(models.Model):
    BH_SKU = models.CharField(max_length=32,primary_key=True)
    BH_Name = models.CharField(max_length=256)
    BH_price = models.DecimalField(max_digits=10,decimal_places=2)
    BH_Status = models.CharField(max_length=32)
    BH_URL = models.CharField(max_length=256)
    BH_UUID = models.CharField(max_length=128)

class AD(models.Model):
    AD_SKU = models.CharField(max_length=32,primary_key=True)
    AD_Name = models.CharField(max_length=256)
    AD_price = models.DecimalField(max_digits=10,decimal_places=2)
    AD_Status = models.CharField(max_length=32)
    AD_URL = models.CharField(max_length=256)
    AD_UUID = models.CharField(max_length=128)
    
class User(models.Model):
    email = models.CharField(max_length=254,primary_key=True)
    password = models.CharField(max_length=256)

class products(models.Model):
    product = models.CharField(max_length=254,primary_key=True)
    MicroCenter_SKU = models.IntegerField()
    BestBuy_SKU = models.IntegerField()
    GameStop_SKU = models.IntegerField()
    Adorama_SKU = models.CharField(max_length=32)
    BH_SKU = models.CharField(max_length=32)
    Amazon_SKU = models.CharField(max_length=32)
    UUID = models.CharField(max_length=128)

