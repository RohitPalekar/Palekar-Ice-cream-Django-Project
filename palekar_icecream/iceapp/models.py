from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class IcecreamInfo(models.Model):
    category = models.CharField(max_length=50)
    iname = models.CharField(max_length=200,verbose_name='Icecream Name')
    desc = models.CharField(max_length=300,verbose_name='Description')
    price = models.IntegerField()
    pic = models.FileField(upload_to='images/')
    det_desc = models.TextField(verbose_name='Detail Description')

class Cart(models.Model):
    uid = models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='uid')
    iid = models.ForeignKey('IcecreamInfo',on_delete=models.CASCADE,db_column='iid')
    qty = models.IntegerField(default=1)

class Order(models.Model):
    uid = models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='uid')
    iid = models.ForeignKey('IcecreamInfo',on_delete=models.CASCADE,db_column='iid')
    qty = models.IntegerField(default=1)
    amt = models.IntegerField()

class OrderHistory(models.Model):
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE, db_column='uid')
    iid=models.ForeignKey('IcecreamInfo',on_delete=models.CASCADE, db_column='iid')
    qty=models.IntegerField(default=1)
    amt=models.IntegerField()

class UserInfo(models.Model):
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE, db_column='uid',verbose_name='User Id')
    mobile = models.CharField(max_length=10)
    address = models.TextField()

class FranchiseQuery(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=10,verbose_name='Contact Number')
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)