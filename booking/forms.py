from django import forms
from .models import Booking
from train.models import TrainSeat

class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

# class BookForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = ['seat']

class BookForm(forms.Form):
    seat = forms.ModelChoiceField(queryset=TrainSeat.objects.all(),label='Select a Seat')
    promo = forms.CharField(max_length=20,label='Promo Code(If you have any)',required=False)