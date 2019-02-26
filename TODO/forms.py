from django import forms
from django.utils import timezone
from django.db import models

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm




class ChangeTask(forms.Form):
    id_field = forms.Field(required=False)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title_field = forms.CharField(label='title', max_length=200)
    text_field = forms.CharField(label='text', max_length=200)
    CHOICES_status = (('не завершено', 'не завершено'), ('выполнено','выполнено'), ('провалено', 'провалено'),)
    status = forms.ChoiceField(label='status', choices=CHOICES_status)
    CHOICES_priority = (('обычный', 'обычный'), ('низкий', 'низкий'), ('высокий', 'высокий'),)
    priority = forms.ChoiceField(label='status', choices=CHOICES_priority)
    create_date = forms.DateTimeField(label='create date', initial=timezone.now)
    expiration_date = forms.DateTimeField(label='expiration date', initial=timezone.now)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Это поле обязательно')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

# class LoginForm(AuthenticationForm):
#
#     class Meta:
#         model = User
#         fields = ('username', 'password', )


