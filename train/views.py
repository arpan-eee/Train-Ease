from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView
from .models import Train,Station,Review
from booking.models import Booking
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

# Create your views here.

class TrainDisplay(ListView):
    template_name = 'train_display.html'
    context_object_name = 'trains'
    model = Train

    def get_queryset(self):
        station_slug = self.kwargs.get('station_slug')
        if station_slug:
            return Train.objects.filter(station__slug=station_slug)
        else:
            return Train.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['station_list'] = Station.objects.all()
        return context
    
def details(request,id):
    train = Train.objects.get(pk=id)
    review = Review.objects.filter(train = train)
    btn = Booking.objects.filter(train = train,user = request.user).exists()

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
