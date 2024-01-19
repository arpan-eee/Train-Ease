from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import UserAccountForm,UserUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.forms import PasswordChangeForm
from booking.models import Booking
from django.contrib.auth.decorators import login_required

def registration(request):
    if request.method == 'POST':
        form = UserAccountForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Please confirm your email address')

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"https://trainease.onrender.com/user/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()


            return redirect('home')
        else:
            messages.error(request, 'There was an error with your submission. Please correct the errors below.')
    else:
        form = UserAccountForm()

    return render(request, 'form.html', {'form': form, 'top': 'Sign Up Form','btn': 'Sign Up'})

@login_required
def update_user_account(request, user_id):
    user_instance = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'User account updated successfully.')
            return redirect('home')
        else:
            messages.warning(request, 'Invalid form submission. Please check the form data.')
    else:
        form = UserUpdateForm(instance=user_instance)
    return render(request, 'form.html', {'form': form, 'top': 'Update Profile Form','btn': 'Update'})


class UserLoginView(LoginView):
    template_name = 'form.html'

    def get_success_url(self):
        return reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, 'Successfully Logged In')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.warning(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top'] = 'Log In Form'
        context['btn'] = 'Log In'
        return context
    
def user_logout(request):
    logout(request)
    return redirect('login')

def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')

@login_required    
def pass_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Updated Successfully')
            update_session_auth_hash(request, form.user)
            return redirect('home')   
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'form.html', {'form' : form, 'top': 'Update Password','btn': 'Update'})

def profile(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'profile.html', {'bookings': bookings})
