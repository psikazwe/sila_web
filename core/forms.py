from typing import Any, Dict
from django import forms
from django.contrib.auth import authenticate, login
from core import models
from datetime import date, timedelta
from django.contrib.auth.forms import UserCreationForm

input_style = 'input'

class DateInput(forms.DateInput):
    input_type = 'date'

class LoginForm(forms.Form):
    email = forms.CharField(max_length=50, label="Email", required=True, widget=forms.TextInput(attrs={'placeholder':'Email'}))
    password = forms.CharField(max_length=500, label="Password", required=True, widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data['email']
        password = cleaned_data['password']
        # do your cleaning here
        if not email:
            raise forms.ValidationError({"email":"email is required"})
        try:
            models.User.objects.get(email__iexact=email)
            if not password:
                raise forms.ValidationError({"password":"Password is required"})
            user = authenticate(email = email, password = password)
            if user:
                login(self.request, user)
                return user
            else:
                raise forms.ValidationError({"password":"Wrong Password"})
        except models.User.DoesNotExist:
            raise forms.ValidationError({"email":'email is invalid'})

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = input_style

class ForgotPasswordForm(forms.Form):
    email = forms.CharField(max_length=50, label="Email", required=True, widget=forms.TextInput(attrs={'placeholder':'Email'}))
    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data['email']
        # do your cleaning here
        if not email:
            raise forms.ValidationError({"email":"email is required"})
        try:
            models.User.objects.get(email__iexact=email)
            return email
        except models.User.DoesNotExist:
            raise forms.ValidationError({"email":"email is not registered with us."})
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = input_style
    
    def getUser(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        return models.User.objects.get(email__iexact=email)