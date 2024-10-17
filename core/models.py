from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from ckeditor.fields import RichTextField

class Company(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos/')


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user
    
    def create_staff(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    def get_media_upload_path(instance, filename):
        return f'/avatars/{instance.email}'
    username = None
    avatar =models.ImageField(upload_to =get_media_upload_path, blank=True)
    firstname = models.CharField(verbose_name='Firstname', max_length=50, blank=True)
    lastname = models.CharField(verbose_name='Lastname', max_length=50, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]
    objects = CustomUserManager()
    def __str__(self):
        return self.email
    
    def role(self):
        if self.is_superuser:
            return str("admin")
        elif self.is_staff:
            return str('staff')
        else:
            return str('client')
    
class OTP(models.Model):
    number = models.IntegerField()
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(blank=True, max_length=10)
    date = models.DateTimeField(default=timezone.now)


class Offer(models.Model):
    def get_media_upload_path(instance, filename):
        return f'{instance.category}/offers/{filename}'
    cover =models.ImageField(upload_to =get_media_upload_path, blank=True)
    name = models.CharField(max_length= 50, unique= True)
    description = models.CharField(max_length= 500)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name
        

class Category(models.Model):
    def get_media_upload_path(instance, filename):
        return f'category/{instance.name}/{filename}'
    name = models.CharField(max_length= 50, unique= True)
    description = models.CharField(max_length= 500)
    cover =models.ImageField(upload_to =get_media_upload_path, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name


class Service(models.Model):
    def get_media_upload_path(instance, filename):
        return f'{instance.category}/services/{filename}'
    name = models.CharField(max_length=50, unique= True)
    description = models.CharField(max_length= 500, blank=True)
    cover =models.ImageField(upload_to =get_media_upload_path, blank=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="services")
    created_on = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name
    def clean(self):
        super(Service, self).clean()  # Call the parent class's clean method
        if '-' in self.name:
            raise ValidationError("The name cannot contain a hyphen.")\
            
    def get_articles(self):
        all = self.articles.all()
        active = all.filter(is_active = True)
        inactive = all.filter(is_active = False)
        return {
            'all': all,
            'active': active,
            'archived': inactive,
        }
        
    def get_promotions(self):
        all = self.promotions.all()
        active = all.filter(is_active = True)
        inactive = all.filter(is_active = False)
        return {
            'all': all,
            'active': active,
            'inactive': inactive,
        }


class Article(models.Model):
    def get_media_upload_path(instance, filename):
        return f'{instance.service.category}/services/{instance.service}/articles/{filename}'
    cover =models.ImageField(upload_to = get_media_upload_path, blank=True)
    title = models.CharField(max_length= 50, unique= True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="articles")
    published_at = models.DateTimeField(default=timezone.now)
    body =  RichTextField(verbose_name = "body", blank = True, null = True)
    is_active = models.BooleanField(default=True)


class Promotion(models.Model):
    def get_media_upload_path(instance, filename):
        return f'{instance.service.category}/services/{instance.service}/promotions/{filename}'
    cover =models.ImageField(upload_to = get_media_upload_path, blank=True)
    title = models.CharField(max_length= 50)
    service =  models.ForeignKey(Service, on_delete=models.CASCADE, related_name="promotions")
    created_on = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    start = models.DateField(blank=False)
    end = models.DateField(blank=False)
    stopped = models.BooleanField( default= False)
    description = models.CharField(max_length=200, blank=True)

from django.core.validators import FileExtensionValidator
class ServiceApplication(models.Model):
    SERVICE_STATUS_CHOICES = [
        ('reviewing', 'Being Reviewed'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('submitted', 'Waiting Review'),
    ]
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="offers")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="applications")
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    nrc_number = models.CharField(max_length=20)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    email = models.EmailField(blank=True, null=True)  # Made optional
    phone_number = models.CharField(max_length=15)
    business_name = models.CharField(max_length=100)
    business_description = models.TextField(max_length=500)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=10, choices=SERVICE_STATUS_CHOICES, default='submitted')  # Default to 'Being Reviewed'
    company_profile = models.FileField(upload_to='company_profiles/', validators=[FileExtensionValidator(['pdf'])], blank=True, null=True)  # Stores PDF documents


class Event(models.Model):
    def get_media_upload_path(instance, filename):
        return f'{instance.service.category}/services/{instance.service}/promotions/{filename}'
    cover =models.ImageField(upload_to = get_media_upload_path, blank=True)
    title = models.CharField(max_length= 50)
    created_on = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    start = models.DateField(blank=False)
    end = models.DateField(blank=False)
    stopped = models.BooleanField( default= False)
    description = models.CharField(max_length=200, blank=True)


class Member(models.Model):
    def get_media_upload_path(instance, filename):
        return f'members/{filename}'
    name = models.CharField(max_length= 100)
    email = models.EmailField(blank=True)
    position = models.CharField(max_length= 100, blank=True)
    description = models.CharField(max_length= 500, blank=True)
    avatar =models.ImageField(upload_to =get_media_upload_path, blank=True)
    is_active = models.BooleanField(default=True)
    facebookURL = models.CharField(max_length= 250, blank= True)
    youtubeURL = models.CharField(max_length= 250, blank= True)
    instagramURL = models.CharField(max_length= 250, blank= True)
    linkedinURL = models.CharField(max_length= 250, blank= True)
    whatsappURL = models.CharField(max_length= 250, blank= True)
    tiktokURL = models.CharField(max_length= 250, blank= True)
    xURL = models.CharField(max_length= 250, blank= True)
    webURL = models.CharField(max_length= 250, blank= True)
    def __str__(self):
        return self.name

class Affiliate(models.Model):
    def get_media_upload_path(instance, filename):
        return f'affliates/{filename}'
    name = models.CharField(max_length= 50, unique= True)
    email = models.EmailField(blank=True)
    code = models.CharField(max_length= 50, unique= True)
    description = models.CharField(max_length= 500)
    logo =models.ImageField(upload_to =get_media_upload_path, blank=True)
    is_active = models.BooleanField(default=True)
    facebookURL = models.CharField(max_length= 250, blank= True)
    youtubeURL = models.CharField(max_length= 250, blank= True)
    instagramURL = models.CharField(max_length= 250, blank= True)
    linkedinURL = models.CharField(max_length= 250, blank= True)
    whatsappURL = models.CharField(max_length= 250, blank= True)
    tiktokURL = models.CharField(max_length= 250, blank= True)
    xURL = models.CharField(max_length= 250, blank= True)
    webURL = models.CharField(max_length= 250, blank= True)
    def __str__(self):
        return self.name
    


class Program(models.Model):
    def get_media_upload_path(instance, filename):
        return f'{instance.category}/program/{filename}'
    cover =models.ImageField(upload_to = get_media_upload_path, blank=True)
    title = models.CharField(max_length= 50, unique= True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="program")
    published_at = models.DateTimeField(default=timezone.now)
    start_at = models.DateTimeField(blank=True, null=True, default=None)
    end_at = models.DateTimeField(blank=True, null=True, default=None)
    body =  RichTextField(verbose_name = "body", blank = True, null = True)
    link = models.CharField(max_length=500, verbose_name='application link')
    is_active = models.BooleanField(default=True)
    stop = models.BooleanField(default=True)
