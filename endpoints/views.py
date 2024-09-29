from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.templatetags.static import static
from django.http import FileResponse
from django.urls import reverse
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import AuthUserSerializer, UserSerializer, UserDetailsSerializer, EmailSerializer
from core.lib.email_services import send_email, send_email_with_attachment
from core.lib.utils import generate_and_save_otps
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from core import models
from endpoints import serializers

@api_view(["GET"])
def us(request):
    logo_url = reverse('logo')
    data = {
        "name": "Sila Global Solutions",
        "initials": "SGS",
        "logo": request.build_absolute_uri(logo_url),
        "description":" We are a what what what",
    }
    return Response(status=status.HTTP_200_OK, data=data)
    
@api_view(["GET"])
def logo(request):
    logo_path = settings.BASE_DIR / 'static' / 'logo.jpg'
    return FileResponse(open(logo_path, 'rb'), content_type='image/jpeg')


class LoginView(TokenObtainPairView):
    serializer_class = AuthUserSerializer


class UserCreateAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.data.get('email')
            url = reverse("confirm_signup")
            confirm_link = request.build_absolute_uri(url)
            full_link = confirm_link+f"?otp={otp}&email={email}"
            otp = generate_and_save_otps(email=email)
            send_email(
                recipient=email, 
                subject="Account Creation", 
                template_name="welcome_email.html",
                context={
                    "welcome_link": full_link,
                    "otp": otp
                }
            )
            return Response({
                "message": "Account successfully created. A confirmation link has been sent to your email",
                "details": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes(['TokenAuthentication'])
@permission_classes([IsAuthenticated])
def account(request):
    # Assuming you want to return the user's username and email
    user_data = {
        'email': request.user.email,
    }
    return Response(user_data, status=status.HTTP_200_OK)

class AccountDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = models.User.objects.get(email__iexact=request.user)
        serializer = UserDetailsSerializer(user)
        return Response(serializer.data)


class SendEmailView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            # Extract data from the serializer
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            from_email = serializer.validated_data['from_email']
            recipient_list = serializer.validated_data['recipient_list']
            attachment = serializer.validated_data['attachment']

            # Save the attachment to a temporary file
            attachment_path = attachment.temporary_file_path()

            # Send the email
            try:
                send_email_with_attachment(subject, message, from_email, recipient_list, attachment_path)
                return Response({"message": "Email sent successfully."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": f"Failed to send email: {e}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CategoriesWithServicesListView(APIView):
    def get(self, request, format=None):
        categories = models.Category.objects.filter(is_active = True)
        count = categories.count()
        serializer = serializers.CategoryWithServicesSerializer(categories, many=True)
        return Response({
            "data": serializer.data,
            "count": count
        })


class OffersListView(APIView):
    def get(self, request, format=None):
        categories = models.Offer.objects.all()
        count = categories.count()
        serializer = serializers.OfferSerializer(categories, many=True)
        return Response({
            "data": serializer.data,
            "count": count
        })

class CategoriesListView(APIView):
    def get(self, request, format=None):
        categories = models.Category.objects.all()
        count = categories.count()
        serializer = serializers.CategorySerializer(categories, many=True)
        return Response({
            "data": serializer.data,
            "count": count
        })
    
    def post(self, request, format=None):
        # Adjusted to exclude 'is_active' since it's not required in the payload
        serializer = serializers.CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This will automatically set 'is_active' to True if not provided
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class CategoryDetailsView(APIView):
    def get(self, request, unique_name, *args, **kwargs):
        normalized_name = unique_name.lower().replace('-', ' ')
        try:
            category_instance = models.Category.objects.filter(name__iexact=normalized_name).first()
            if category_instance:
                serializer = serializers.CategoryWithServicesSerializer(category_instance)
                return Response(serializer.data)
            else:
                return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ServicesListView(APIView):
    def get(self, request, format=None):
        services = models.Service.objects.filter(is_active=True)
        count = services.count()
        serializer = serializers.ServiceSerializer(services, many=True, context={'request': request})
        return Response({
            "data": serializer.data,
            "count": count
        })
    
    def post(self, request, format=None):
        serializer = serializers.ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ServiceDetailsView(APIView):
    def get(self, request, unique_name, *args, **kwargs):
        normalized_name = unique_name.lower().replace('-', ' ')
        try:
            service_instance = models.Service.objects.filter(name__iexact=normalized_name).first()
            if service_instance:
                serializer = serializers.ServiceSerializer(service_instance, context={'request': request})
                return Response(serializer.data)
            else:
                return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ServiceApplicationCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.ServiceApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticlesListView(APIView):
    def get(self, request, format=None):
        articles = models.Article.objects.all()
        count = articles.count()
        serializer = serializers.ArticleSerializer(articles, many=True)
        return Response({
            "data": serializer.data,
            "count": count
        })
    
    def post(self, request, format=None):
        serializer = serializers.ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersListView(APIView):
    def get(self, request, format=None):
        articles = models.User.objects.all()
        count = articles.count()
        serializer = serializers.UserListSerializer(articles, many=True)
        return Response({
            "data": serializer.data,
            "count": count
        })
    
    def post(self, request, format=None):
        serializer = serializers.UserListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)