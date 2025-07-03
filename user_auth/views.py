from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, UserLoginForm, OTPForm
from django.views.generic import CreateView, FormView
from django.contrib import messages
from django.urls import reverse_lazy
import random
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
# Create your views here.
#helper function to generate otp
def generate_otp():
    return int(random.randint(100000, 999999))

class OTPVerifyView(FormView):
    template_name = 'user_auth/otp_verify.html'
    form_class = OTPForm
    success_url = reverse_lazy('otp_verify')

    def form_valid(self, form):
        entered_otp = form.cleaned_data['otp']
        session_otp = self.request.session.get('otp')
        user_id = self.request.session.get('otp_user_id')
        if entered_otp == session_otp and user_id:
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            # Clean up session
            del self.request.session['otp']
            del self.request.session['otp_user_id']
            messages.success(self.request, 'Your account has been activated! You can now log in.')
            return redirect('login')
        else:
            messages.error(self.request, 'Invalid OTP. Please try again.')
            return self.form_invalid(form)

class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'user_auth/register.html'
    success_url = reverse_lazy('login')  
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        otp=generate_otp()
        self.request.session['otp'] = otp
        self.request.session['otp_user_id'] = user.id
        send_mail(
            subject='Your OTP Code',
            message=f'Your verification code is: {otp}',
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )
        messages.success(self.request, 'Account created! Check your email for the OTP.')
        return redirect('otp_verify')

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class UserLoginView(FormView):
    template_name = 'user_auth/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('file_upload:list_file')  
    
    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'Login successful!')
            return redirect('file_upload:list_file')
        else:
            messages.error(self.request, 'Invalid username or password.')
            return super().form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)



