from django.contrib.auth import forms

from .models import User


class CustomUserCreationForm(forms.UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name',)


class CustomUserChangeForm(forms.UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name',)
