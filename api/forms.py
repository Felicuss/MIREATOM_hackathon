from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, label="Имя")
    last_name = forms.CharField(max_length=100, required=True, label="Фамилия")
    email = forms.EmailField(max_length=255, required=True, label="Почта")

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']
