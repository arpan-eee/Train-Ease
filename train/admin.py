from django.contrib import admin
from .models import Compartment,Seat,Train,Review,Station,TrainSeat,Promo

# Register your models here.

admin.site.register(Compartment)
admin.site.register(Seat)
admin.site.register(Train)
admin.site.register(Review)
admin.site.register(Station)
admin.site.register(TrainSeat)
admin.site.register(Promo)
# admin.site.register(TrainFare)
