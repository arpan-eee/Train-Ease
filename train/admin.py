from django.contrib import admin
from .models import Compartment,Seat,Train,Review,Station

# Register your models here.

admin.site.register(Compartment)
admin.site.register(Seat)
admin.site.register(Train)
admin.site.register(Review)
admin.site.register(Station)
