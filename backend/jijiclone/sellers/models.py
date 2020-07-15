from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.

class Seller(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    state_of_residence = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 100, unique=True)
    password = models.CharField(max_length = 255)

    def __str__(self):
        return self.email

class Buyer(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField(max_length=100, unique=True)
    location = models.CharField(max_length = 50)

class Item(models.Model):
    name = models.CharField(max_length = 255)
    price = models.IntegerField()
    description = models.TextField()
    imageUrl = models.CharField(max_length = 200)
    slug = models.CharField(max_length = 200, unique=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='items')
    is_sold = models.BooleanField(default=0)
    interested_buyers = models.ManyToManyField(Buyer, related_name='items',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
