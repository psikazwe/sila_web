from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path("", views.us, name="company_details"),
    path("logo", views.logo, name="logo"),
    path("login", views.LoginView.as_view(), name="login"),
    path('signup', views.UserCreateAPIView.as_view(), name='signup'),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('account', views.AccountDetailsView.as_view(), name='account'),

    path('offers/', views.OffersListView.as_view(), name='offers-list'),

    path('categories', views.CategoriesListView.as_view(), name='categories-list'),
    path('categories/services', views.CategoriesWithServicesListView.as_view(), name='categories-services'),
    path('categories/<str:unique_name>', views.CategoryDetailsView.as_view(), name='category_detail'),

    path('apply/services', views.ServiceApplicationCreateView.as_view(), name='apply-services'),
    path('services', views.ServicesListView.as_view(), name='services-list'),
    path('services/<str:unique_name>', views.ServiceDetailsView.as_view(), name='service_detail'),

    path('articles', views.ArticlesListView.as_view(), name='articles-list'),

    path('users', views.UsersListView.as_view(), name='users-list'),

]
