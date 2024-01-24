from django.shortcuts import render
from train.forms import ComplaintForm

def home(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ComplaintForm()
    return render(request, 'home.html',{'form':form})