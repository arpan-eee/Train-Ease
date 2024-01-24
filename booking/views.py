from django.shortcuts import render,get_object_or_404,redirect
from .forms import DepositForm,BookForm
from .models import Deposit,Booking
from django.contrib import messages
from train.models import Train , Promo
from django.contrib.auth.decorators import login_required
from decimal import Decimal

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
            promo = form.cleaned_data.get('promo')
            print(promo)
            if seat.is_booked:
                messages.warning(request,"Seat is already Booked")
            elif passenger.balance < seat.train.ticket_price:
                messages.warning(request,"Insufficiant Balance")
            elif not promo:

                booking = Booking(train=seat.train , user=request.user,seat = seat)
                booking.save()

                passenger.balance -= seat.train.ticket_price
                passenger.save()
                messages.success(request,"Successfully Purchased Ticket")

                seat.is_booked = True
                seat.save()

            else:
                if Promo.objects.filter(code = promo.upper()).exists(): 
                    promo_model = Promo.objects.get(code = promo.upper())
                    if promo_model.user.filter(pk=request.user.pk).exists():
                        messages.warning(request,"You already used this Promo Code Once")
                    else:
                        promo_model.user.add(request.user)
                        promo_model.save()

                        booking = Booking(train=seat.train , user=request.user,seat = seat)
                        booking.save()

                        passenger.balance -= Decimal((int(seat.train.ticket_price) * (100-int(promo_model.amount))) / 100)
                        passenger.save()
                        messages.success(request,"Successfully Purchased Ticket On Discount")

                        seat.is_booked = True
                        seat.save()

                else:
                    messages.warning(request,"Invalid Promo Code")
            return redirect('home')
    else:
        form = BookForm()

    return render(request, 'booking.html', {'form': form})

