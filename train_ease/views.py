from django.shortcuts import render
from train.forms import ComplaintForm

def home(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        try:
            form = ComplaintForm(instance=request.user)
        except:
            form = ComplaintForm()
    return render(request, 'home.html',{'form':form})