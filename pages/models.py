from django.db import models

# Create your models here.

#BestBuy table
class BestBuy(models.Model):
    SKU = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=256)
    price = models.FloatField()
    Status = models.CharField(max_length=32)
    URL = models.CharField(max_length=256)
    Reviews = models.FloatField()