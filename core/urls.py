from django.urls import path
from .views import index, confirm_signup, Logout, Login
from . import views

urlpatterns = [
    path("", index, name="landing"),
    path("confirm_signup", confirm_signup, name="confirm_signup"),
    path('logout',Logout, name='logout'),
    path('login',Login, name='login'),
    path('book', views.book_meeting, name='book'),
    path("about", views.AboutUsView.as_view(), name="us"),
    path("event", views.EventListView.as_view(), name="event"),
    path("promotion", views.AboutUsView.as_view(), name="promotion"),
    path("industry", views.CategoryListView.as_view(), name="industry"),
    path("service", views.ServiceListView.as_view(), name="service"),
    path("service/<int:pk>", views.ServiceDetailView.as_view(), name="service-detail"),
    path("blog", views.AboutUsView.as_view(), name="blog"),
    path("team", views.TeamView.as_view(), name="team"),

]
