from django import forms
from core.models import Service, Category, Article, User, OTP, Affiliate, Member
from django.urls import reverse
from core.lib.utils import generate_random_password


class CategoryForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': '5'}))
    class Meta:
        model = Category
        fields = ['name', 'description', 'is_active', 'cover']

class ServiceForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': '5'}))
    cover = forms.ImageField(widget=forms.FileInput, required=False)
    class Meta:
        model = Service
        fields = ['name', 'description', 'cover', 'is_active', 'category']    
        

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'service', 'cover', 'body', ]

class AffiliateForm(forms.ModelForm):
    class Meta:
        model = Affiliate
        fields = '__all__'
        
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
        

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'email', 'is_active']

from core.lib.email_services import send_email
from core.lib.utils import generate_and_save_otps
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

class UserCreationForm(forms.Form):
    role = forms.ChoiceField(choices=[
        ('ADMIN', 'Admin'),
        ('STAFF', 'Staff'),
        ('CLIENT', 'Client')
    ], required=True)
    email = forms.EmailField(label="Email", required=True)

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        
        if OTP.objects.filter(email=email).exists():
            raise ValidationError("Account already created. Pending activation")
        
        # Additional email validation
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise ValidationError("Please enter a valid email address.")
        
        return email

    def save(self):
        cleaned_data = self.cleaned_data
        otp = generate_and_save_otps(**cleaned_data)
        if not otp:
            return  ValidationError("OTP generation false.")
        return cleaned_data


class NewUserForm(forms.ModelForm):
    role = forms.ChoiceField(choices=[
        ('ADMIN', 'Admin'),
        ('STAFF', 'Staff'),
        ('CLIENT', 'Client')
    ], required=True)

    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'email']

    def save(self, commit = False):
        role = self.cleaned_data.get('role')
        if role == 'ADMIN':
            self.instance.is_superuser = True
        if role == 'STAFF':
            self.instance.is_staff = True
        password = generate_random_password()
        self.instance.set_password(password)
        if commit:
            send_email(
                recipient=self.instance.email, 
                subject= "Account created", 
                template_name="email/account_created.html", 
                context= { 
                    "email": self.instance.email,
                    "password": password,
                }
            )
        return super().save(commit)



class UserTokenVerifyForm(forms.Form):
    email = forms.EmailField(label="Email", required=True)
    token = forms.IntegerField(label="Token", required=True)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if OTP.objects.filter(email=email).exists():
            return email
        raise ValidationError("No pending account creation for this email")
    
    def clean_token(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        token = cleaned_data.get('token')
        
        if token < 100000 or token > 999999:
            raise ValidationError("Invalid token")
        
        if not OTP.objects.filter(email=email, number=token).exists():
            raise ValidationError("Invalid verification token")
        
        return token
    
    def save(self):
        cleaned_data = super().clean()
        token = cleaned_data.get('token')
        otp = OTP.objects.get(number=token)
        if otp.role == 'ADMIN':
            user = User.objects.create_superuser(email = otp.email, password = generate_random_password())
        elif otp.role == 'STAFF':
            user = User.objects.create_staff(email = otp.email, password = generate_random_password())
        else:
            user = User.objects.create_user(email = otp.email, password = generate_random_password())
        otp.delete()
        return user
        
    