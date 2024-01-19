from django.db import models
from train.models import Seat,Train
from django.contrib.auth.models import User


# Create your models here.

class Booking(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE,null=True, blank=True)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE,null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.train.name} by {self.user.username} at {self.time}"
    
class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)