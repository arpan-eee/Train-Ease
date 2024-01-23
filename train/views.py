from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView
from .models import Train,Station,Review
from booking.models import Booking
from .forms import ReviewForm,SearchForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

class TrainDisplay(ListView):
    template_name = 'train_display.html'
    context_object_name = 'trains'
    model = Train

    def get_queryset(self):
        station_slug = self.kwargs.get('station_slug')
        if station_slug:
            return Train.objects.filter(Q(to_station__slug=station_slug) | Q(from_station__slug=station_slug))
        else:
            return Train.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['station_list'] = Station.objects.all()
        return context
    
def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            from_station = form.cleaned_data['from_station']
            to_station = form.cleaned_data['to_station']
            # Process the form data
            station_list = Station.objects.all()
            trains = Train.objects.filter(to_station=to_station , from_station=from_station)
            return render(request, 'train_display.html', {'station_list': station_list, 'trains': trains})
    else:
        form = SearchForm()
    return render(request, 'search_train.html', {'form': form})
    
def user_comment(request,id):
    train = get_object_or_404(Train, id=id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.train = train
            review.save()
            return redirect('home')
    else:
        form = ReviewForm()
    return render(request, 'comment.html', {'form': form})
    
def details(request,id):
    train = Train.objects.get(pk=id)
    review = Review.objects.filter(train = train)
    try:
        btn = Booking.objects.filter(train = train,user = request.user).exists()
    except:
        btn = False

    return render(request,'details.html',{'train' : train,'comments': review,'btn' : btn})


def user_comment(request,id):
    train = get_object_or_404(Train, id=id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.train = train
            review.save()
            return redirect('home')
    else:
        form = ReviewForm()

    return render(request, 'comment.html', {'form': form})


