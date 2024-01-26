from django.db import models
from django.contrib.auth.models import User
from django.forms import TimeInput
from django.utils.text import slugify
from django.core.validators import MaxValueValidator

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
    seat_number = models.IntegerField()

    def __str__(self):
        return f"{self.seat_number}"
    
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
    from_station = models.ForeignKey(Station, blank=True, null=True, on_delete=models.CASCADE,related_name='from_station')
    to_station = models.ForeignKey(Station, blank=True, null=True, on_delete=models.CASCADE,related_name='to_station')
    departure = models.TimeField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2 , blank=True, null=True)
    image = models.ImageField(upload_to='train/media/uploads/', blank = True, null = True)

    def __str__(self):
        return self.name
    
class TrainSeat(models.Model):
    train = models.ForeignKey(Train, blank=True, null=True,on_delete=models.CASCADE)
    compartment = models.ForeignKey(Compartment, blank=True, null=True, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, blank=True, null=True, on_delete=models.CASCADE)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        seat_status_str = "Not Available" if self.is_booked else "Available"
        return f"{self.train}  |  {self.compartment}  -  {self.seat}  | Price : {self.train.ticket_price} |  {seat_status_str}"
    
# class TrainFare(models.Model):
#     train = models.ForeignKey(Train, blank=True, null=True,on_delete=models.CASCADE)
#     from_station = models.ForeignKey(Station, blank=True, null=True, on_delete=models.CASCADE,related_name='from_trainfare')
#     to_station = models.ForeignKey(Station, blank=True, null=True, on_delete=models.CASCADE,related_name='to_trainfare')
#     taka = models.DecimalField(max_digits=10, decimal_places=2)
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    rating = models.CharField(max_length=5, choices=STAR_CHOICES)
    comment = models.TextField()

    def __str__(self):
        return f"Review by {self.user.username} for {self.train.name}"
    
class Promo(models.Model):
    code = models.CharField(max_length=20)
    user = models.ManyToManyField(User, blank=True, null=True)
    amount = models.IntegerField(validators=[MaxValueValidator(limit_value=100)])

    def __str__(self):
        return f"{self.code}"
    
class Complaint(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    text = models.TextField()
    seen = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        seen_status = "Reviewed" if self.seen else "Pending Review"
        return f"{self.name} - {self.email} - {self.time} - {seen_status}"
