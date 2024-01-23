from django import forms
from .models import Review,Station

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating','comment']

class SearchForm(forms.Form):
    from_station = forms.ModelChoiceField(queryset=Station.objects.all(), empty_label="Select a station .")
    to_station = forms.ModelChoiceField(queryset=Station.objects.all(), empty_label="Select a station .")