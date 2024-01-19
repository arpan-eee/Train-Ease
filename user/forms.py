from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Passenger


class UserAccountForm(UserCreationForm):
    nid = forms.CharField(max_length=20)
    phone = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2','phone','nid']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.is_active = False
            user.save()
            Passenger.objects.create(user=user, phone=self.cleaned_data['phone'], nid=self.cleaned_data['nid'])
        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class UserUpdateForm(forms.ModelForm):
    nid = forms.CharField(max_length=20)
    phone = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            try:
                user_passenger = self.instance.passenger
            except Passenger.DoesNotExist :
                user_passenger = None

            if user_passenger:
                self.fields['nid'].initial = user_passenger.nid
                self.fields['phone'].initial = user_passenger.phone

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            user_passenger, created = Passenger.objects.get_or_create(user=user)

            user_passenger.nid = self.cleaned_data['nid']
            user_passenger.phone = self.cleaned_data['phone']
            user_passenger.save()

        return user

