from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import FormView
from django.urls import reverse_lazy

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already in use.")
        return username

    def form_valid(self, form):
        messages.success(self.request, 'Account created! Check your email for the OTP.')
        return redirect('otp_verify')


class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not username and not password:
            raise forms.ValidationError("Please enter a username and password.")

class OTPForm(forms.Form):
    otp = forms.IntegerField(label='Enter OTP', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter OTP'}))

class OTPVerifyView(FormView):
    template_name = 'user_auth/otp_verify.html'
    form_class = OTPForm
    success_url = reverse_lazy('login')

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