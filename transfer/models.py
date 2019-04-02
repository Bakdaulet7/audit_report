from django.db import models

class Merchant(models.Model):
    counterparty = models.CharField(max_length=50,null =True)
    sector = models.CharField(max_length = 30,null =True)
    sku = models.CharField(max_length = 50,null =True)
    brand = models.CharField(max_length = 50,null =True)
    date = models.DateField(null =True)
    status = models.IntegerField(null =True)

class Brand(models.Model):
    code = models.CharField(max_length = 50,default='SOME STRING')
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name