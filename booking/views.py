from django.shortcuts import render,get_object_or_404,redirect
from .forms import DepositForm,BookForm
from .models import Deposit,Booking
from django.contrib import messages
from train.models import Train
from django.contrib.auth.decorators import login_required

# Create your views here.

def deposit_view(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount >= 200:
                passenger = request.user.passenger
                passenger.balance += amount
                passenger.save()
                Deposit.objects.create(user=request.user, amount=amount,balance_after = passenger.balance)
                messages.success(request,"Deposit Money Successful")
                return redirect('home')
            else:
                messages.warning(request,"Minimum deposit amount is 200")
                return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = DepositForm()

    return render(request, 'form.html', {'form': form, 'top': 'Deposit Form','btn': 'Deposit'})

def TicketBooking(request):
    passenger = request.user.passenger

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            seat = form.cleaned_data['seat']
            if seat.is_booked:
                messages.warning(request,"Seat is already Booked")
            elif passenger.balance >= seat.train.ticket_price:
                
                booking = Booking(train=seat.train , user=request.user,seat = seat)
                booking.save()

                passenger.balance -= seat.train.ticket_price
                passenger.save()
                messages.success(request,"Successfully Purchased Ticket")

                seat.is_booked = True
                seat.save()

            else:
                messages.warning(request,"Insufficiant Balance")
            return redirect('home')
    else:
        form = BookForm()

    return render(request, 'booking.html', {'form': form})

