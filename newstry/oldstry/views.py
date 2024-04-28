from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, PasswordResetForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.core.mail import send_mail
#from django.template.loader import render_to_string
#from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail

# Create your views here.
def index(request):
    return render(request, 'oldstry/index.html')

def register(request):
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            messages.success(request, 'Account Created Successfully')
            form.save()
            return redirect('user_login')
    else:
        form = SignUpForm()
    return render(request, 'oldstry/admin/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.error(request,'Invalid username and password')
            elif user.is_active:
                login(request, user)
                return redirect('dashboard')
        else:
            print(form.errors)
    else:
        form = AuthenticationForm()
    return render(request, 'oldstry/admin/user_login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('user_login')

def dashboard(request):
    
    return render(request, 'oldstry/admin/dashboard.html')

def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(data=request.POST)
        if form.is_valid():
            subject = 'Reset Password'
            message = 'This is the reset password message that is sent to your given email id'
            from_email = 'pramit.acharya27@gmail.com'
            recipient_list = [form.cleaned_data.get('email')]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False,)
            return redirect('verify_code')
    else:
            form = PasswordResetForm()
            return render(request, 'oldstry/admin/forgot_password.html', {'form': form})
def verify_code(request):
    if request.method == 'POST':
        verification_code = request.POST['verification_code']
        new_password= request.POST['new_password']
        user_email = request.POST['email']
        user = get_user_model().objects.get(email=user_email)
        if user and user.verification_code == verification_code:
            user.set_password(new_password)
            user.save()
            return redirect('reset_password')
        else:
            pass
    return render(request, 'oldstry/admin/verify_code.html')

def password_reset_form(request):
    return render(request, 'oldstry/admin/password_reset_form.html')

#def password_reset_confirm(request):
#    return render(request, 'oldstry/admin/password_reset_confirm.html')
