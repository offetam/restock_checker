from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE

# Create your models here.
class products(models.Model):
    product = models.CharField(max_length=254)
    UUID = models.CharField(max_length=128,primary_key=True)

#BestBuy table
class BestBuy(models.Model):
    BestBuy_price = models.DecimalField(max_digits=10,decimal_places=2)
    BestBuy_Status = models.CharField(max_length=32)
    BestBuy_Ratings = models.DecimalField(max_digits=3,decimal_places=2)
    BestBuy_Review = models.IntegerField()
    BestBuy_ModelNumber = models.CharField(max_length=128)
    BestBuy_SKU = models.IntegerField(primary_key=True)
    BestBuy_URL = models.CharField(max_length=256)
    BestBuy_UUID = models.ForeignKey(products,on_delete=CASCADE)

class MicroCenter(models.Model):
    MicroCenter_Price = models.DecimalField(max_digits=10,decimal_places=2)
    MicroCenter_SKU = models.IntegerField(primary_key=True)
    MicroCenter_ModelNumber = models.CharField(max_length=128)
    MicroCenter_URL = models.CharField(max_length=256)
    MicroCenter_UUID = models.ForeignKey(products,on_delete=CASCADE)

class Gamestop(models.Model):
    Gamestop_SKU = models.CharField(max_length=32,primary_key=True)
    Gamestop_price = models.DecimalField(max_digits=10,decimal_places=2)
    Gamestop_URL = models.CharField(max_length=256)
    Gamestop_Status = models.CharField(max_length=32)
    Gamestop_UUID = models.ForeignKey(products,on_delete=CASCADE)
    Gamestop_Ratings = models.DecimalField(max_digits=3,decimal_places=2)
    Gamestop_Reviews = models.IntegerField()

class BH(models.Model):
    BH_SKU = models.CharField(max_length=32,primary_key=True)
    BH_price = models.DecimalField(max_digits=10,decimal_places=2)
    BH_Status = models.CharField(max_length=32)
    BH_URL = models.CharField(max_length=256)
    BH_UUID = models.ForeignKey(products,on_delete=CASCADE)
    BH_Ratings = models.DecimalField(max_digits=3,decimal_places=2)
    BH_Reviews = models.IntegerField()

class AD(models.Model):
    AD_SKU = models.CharField(max_length=32,primary_key=True)
    AD_price = models.DecimalField(max_digits=10,decimal_places=2)
    AD_Status = models.CharField(max_length=32)
    AD_URL = models.CharField(max_length=256)
    AD_UUID = models.ForeignKey(products,on_delete=CASCADE)
    AD_Ratings = models.DecimalField(max_digits=3,decimal_places=2)
    AD_Reviews = models.IntegerField()

class Amazon(models.Model):
    Amazon_SKU = models.CharField(max_length=32,primary_key=True)
    Amazon_price = models.DecimalField(max_digits=10,decimal_places=2)
    Amazon_Ratings = models.DecimalField(max_digits=3,decimal_places=2)
    Amazon_Reviews = models.IntegerField()
    Amazon_Status = models.CharField(max_length=64)
    Amazon_URL = models.CharField(max_length=512)
    Amazon_UUID =models.ForeignKey(products,on_delete=CASCADE)

class User(models.Model):
    email = models.CharField(max_length=254,primary_key=True)
    password = models.CharField(max_length=256)
    verificationCode = models.IntegerField()
    verify = models.IntegerField(default=0)
    numTry = models.IntegerField(default=0)

class Notification(models.Model):
    IDUUID = models.AutoField(primary_key=True)
    email = models.CharField(max_length=254)
    product = models.CharField(max_length=254)