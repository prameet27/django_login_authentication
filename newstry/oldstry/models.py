from django.db import models
from django.contrib.auth.models import User
from django import forms
# Create your models here.

class SignUpProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username 