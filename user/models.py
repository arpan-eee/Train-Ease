from django.db import models
from django.contrib.auth.models import User


class Passenger(models.Model):
    user = models.OneToOneField(User, related_name='passenger', on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    nid = models.CharField(unique = True ,max_length=20)
    phone = models.CharField(max_length=20)
    admin_status = models.BooleanField(default=False,blank=True,null=True)
    
    def __str__(self):
        return self.nid