from django.urls import path
from .views import deposit_view,TicketBooking

urlpatterns = [
    path('deposit/', deposit_view , name = 'deposit'),
    path('ticket/<int:id>', TicketBooking , name = 'booking'),
]