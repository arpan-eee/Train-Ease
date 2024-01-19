from django.db import models
from django.contrib.auth.models import User
from django.forms import TimeInput
from django.utils.text import slugify

STAR_CHOICES = [
        ('⭐', '⭐'),
        ('⭐⭐', '⭐⭐'),
        ('⭐⭐⭐', '⭐⭐⭐'),
        ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
        ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
    ]


class Compartment(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Seat(models.Model):
    compartment = models.ForeignKey(Compartment, on_delete=models.CASCADE)
    seat_number = models.IntegerField()

    def __str__(self):
        return f"Compartment {self.compartment.name} - Seat {self.seat_number}"
    
class Station(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Train(models.Model):
    name = models.CharField(max_length=100)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    station = models.ForeignKey(Station, blank=True, null=True,on_delete=models.CASCADE)
    departure = models.DateTimeField()

    def __str__(self):
        return self.name
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    rating = models.CharField(max_length=5, choices=STAR_CHOICES)
    comment = models.TextField()

    def __str__(self):
        return f"Review by {self.user.username} for {self.train.name}"
