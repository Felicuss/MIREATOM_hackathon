from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from .models import CustomUser
from django.db import models

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, label="Имя")
    last_name = forms.CharField(max_length=100, required=True, label="Фамилия")
    email = forms.EmailField(max_length=255, required=True, label="Почта")
    profile_picture = models.ImageField(
        upload_to='profile_pics/', null=True, blank=True
    )
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']


class CustomUserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'profile_picture']  # Добавляем поле для профиля