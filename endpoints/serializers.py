from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound
from core.models import Company
from core import models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.db.models import Prefetch

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'logo']


class AuthUserSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Add custom claims
        data.update({
            "username": self.user.username,
            "active": self.user.is_active,
            "email": self.user.email,
            "permissions": self.user.user_permissions.values_list("codename", flat=True),
            "groups": self.user.groups.values_list("name", flat=True),
        })
        return data


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('email', 'is_active')


class EmailSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()
    from_email = serializers.EmailField()
    recipient_list = serializers.ListField(child=serializers.EmailField())
    attachment = serializers.FileField()

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Offer 
        fields = ('__all__')


class CategoryWithServicesSerializer(serializers.ModelSerializer):
    services = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = ['name', 'description', 'is_active', 'services']

    def get_services(self, obj):
        # Define a prefetch object to limit the fields returned for each service
        services_prefetch = Prefetch(
            'services',
            queryset=models.Service.objects.only('name'),
            to_attr='limited_services'
        )
        # Retrieve the category with the prefetched services
        category_with_services = models.Category.objects.prefetch_related(services_prefetch).get(pk=obj.pk)
        # Extract the limited service names
        service_names = [service.name for service in category_with_services.limited_services]

        return service_names

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'name', 'description', 'is_active']
        read_only_fields = ('is_active',)
    def create(self, validated_data):
        instance = models.Category.objects.create(**validated_data)
        return instance

class ServiceSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.CharField(write_only=True)

    cover = serializers.ImageField(read_only=True)
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if representation['cover']:
            representation['cover'] = request.build_absolute_uri(representation['cover'])
        return representation

    class Meta:
        model = models.Service
        fields = ['id', 'name', 'description', 'cover', 'is_active', 'created_on', 'category', 'category_id']
        read_only_fields = ('created_on', 'is_active')
        depth = 1
    def create(self, validated_data):
            try:
                category_id = validated_data['category_id']
                category = models.Category.objects.get(id=category_id)
            except models.Category.DoesNotExist:
                raise NotFound("Category not found.")
            except Exception as e:
                raise ValidationError(f"Invalid category ID: {e}")
            try:
                instance = models.Service.objects.create(category=category, **validated_data)
            except Exception as e:
                raise ValidationError(f"Failed to create service: {e}")
            return instance
    

from datetime import datetime
# Define the validation function
def validate_date_of_birth(value):
    try:
        print(value)
        datetime.strptime(value, '%Y-%m-%d')
    except ValueError:
        raise serializers.ValidationError("Date has wrong format. Use one of these formats instead: YYYY-MM-DD.")

from datetime import datetime
from django.utils.translation import gettext_lazy as _
class ServiceApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceApplication
        fields = '__all__' 
        extra_kwargs = {'email': {'required': False}}
    def clean_date_of_birth(self):
        """
        Validate that the date_of_birth is in the correct format.
        """
        date_of_birth = self.initial_data.get('date_of_birth')
        if date_of_birth:
            try:
                print(date_of_birth)
                datetime.strptime(date_of_birth, '%Y-%m-%d')
            except ValueError:
                raise serializers.ValidationError(_("Date has wrong format. "))
        return date_of_birth
    
    def create(self, validated_data):
        company_profile = validated_data.pop('company_profile')
        instance = models.ServiceApplication.objects.create(**validated_data)
        instance.company_profile.save(company_profile.name, company_profile)
        return instance

class ArticleSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_id = serializers.CharField(write_only=True)
    class Meta:
        model = models.Article
        fields = ['id', 'title', 'cover', 'published_at', 'body', 'service', 'service_id']
        read_only_fields = ('id')
        depth = 1
    def create(self, validated_data):
            try:
                service_id = validated_data['service_id']
                service = models.Service.objects.get(id=service_id)
            except models.Service.DoesNotExist:
                raise NotFound("Service not found.")
            except Exception as e:
                raise ValidationError(f"Invalid service ID: {e}")
            try:
                instance = models.Article.objects.create(service=service, **validated_data)
            except Exception as e:
                raise ValidationError(f"Failed to create service: {e}")
            return instance
    


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'email', 'is_active', 'is_staff', 'is_superuser', 'firstname', 'lastname']
        read_only_fields = ('is_active',)
    def create(self, validated_data):
        instance = models.User.objects.create(**validated_data)
        return instance