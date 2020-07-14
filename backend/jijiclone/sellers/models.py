from django.db import models

# Create your models here.

class Seller(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    state_of_residence = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 100, unique=True)
    password = models.CharField(max_length = 255)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

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
    slug = models.CharField(max_length = 200)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='items')
    is_sold = models.BooleanField(default=0)
    interested_buyers = models.ManyToManyField(Buyer, related_name='items',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
