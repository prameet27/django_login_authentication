from django import forms
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.backends import ModelBackend
#from django.contrib.auth import authenticate, login, logout
#from oldstry import views
from django.core.mail import send_mail
from django.template.loader import render_to_string
#from django.utils.html import strip_tags
from django.contrib.auth import get_user_model

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
        return user

class LoginForm(forms.Form):  # Changed inheritance to forms.Form
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class CustomPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = render_to_string(subject_template_name, context)
        # Remove newlines
        subject = ''.join(subject.splitlines())

        message = render_to_string(email_template_name, context)

        if html_email_template_name is not None:
            html_message = render_to_string(html_email_template_name, context)
        else:
            html_message = None

        send_mail(subject, message, from_email, [to_email], html_message=html_message)


class MyBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            return user
        else:
            return None



