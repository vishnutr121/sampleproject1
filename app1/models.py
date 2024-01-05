from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categories(models.Model):
    category_name=models.CharField(max_length=255)
    category_image=models.ImageField(blank=True,upload_to='category/',null=True)

class Donor(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    phone_number=models.CharField(max_length=255)
    address=models.TextField()
    image=models.ImageField(blank=True,upload_to='donor/',null=True)

class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    phone_number=models.CharField(max_length=255)
    address=models.TextField()
    image=models.ImageField(blank=True,upload_to='customer/',null=True)

class Pet(models.Model):
    category=models.ForeignKey(Categories,on_delete=models.CASCADE,null=True)
    donor=models.ForeignKey(Donor,on_delete=models.CASCADE,null=True)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    pet_name=models.CharField(max_length=255)
    pet_description=models.TextField()
    price=models.IntegerField()
    pet_image=models.ImageField(blank=True,upload_to='pets/',null=True)
    approval=models.CharField(max_length=255,default='false')
    buystatus=models.CharField(max_length=255,default='not sold')
    captcha=models.IntegerField(default=0)
    pets_view=models.CharField(max_length=255,default='false')

class Petcart(models.Model):
    pet=models.ForeignKey(Pet,on_delete=models.CASCADE,null=True)
    customer=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

class SalesCount(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    sales=models.IntegerField(default=0)
    oldsales=models.IntegerField(default=0)
    olddisapprove=models.IntegerField(default=0)
    newdisapprove=models.IntegerField(default=0)

class HomePets(models.Model):
    home_pet_name=models.CharField(max_length=255)
    home_price=models.IntegerField()
    home_pet_image=models.ImageField(blank=True,upload_to='homepets/',null=True)
    offer_percent=models.IntegerField(default=0)