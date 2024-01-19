from django.shortcuts import render,get_object_or_404,redirect
from .forms import DepositForm,BookForm
from .models import Deposit
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

def TicketBooking(request,id):
    train = get_object_or_404(Train, id=id)
    passenger = request.user.passenger

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            if passenger.balance >= train.ticket_price:
                booking = form.save(commit=False)
                booking.user = request.user
                booking.train = train
                booking.save()
                passenger.balance -= train.ticket_price
                passenger.save()
                messages.success(request,"Successfully Purchased Ticket")
            else:
                messages.warning(request,"Insufficiant Balance")
            return redirect('home')
    else:
        form = BookForm()

    return render(request, 'booking.html', {'form': form})