from django import forms
from .models import Booking

class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

class BookForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['seat']