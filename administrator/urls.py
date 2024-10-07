from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # affilates url 
    path('affiliates', views.AffiliateListView.as_view(), name='affiliate-list'),
    path('affiliates/<int:pk>', views.AffiliateDetailView.as_view(), name='affiliate-detail'),
    path('affiliates/create', views.AffiliateCreateView.as_view(), name='affiliate-create'),
    path('affiliates/<int:pk>/update', views.AffiliateUpdateView.as_view(), name='affiliate-update'),
    path('affiliates/<int:pk>/delete', views.AffiliateDeleteView.as_view(), name='affiliate-delete'),
    
    # affilates url 
    path('members', views.MemberListView.as_view(), name='member-list'),
    path('members/<int:pk>', views.MemberDetailView.as_view(), name='member-detail'),
    path('members/create', views.MemberCreateView.as_view(), name='member-create'),
    path('members/<int:pk>/update', views.MemberUpdateView.as_view(), name='member-update'),
    path('members/<int:pk>/delete', views.MemberDeleteView.as_view(), name='member-delete'),

    # services 
    path('services', views.ServiceListView.as_view(), name='service-list'),
    path('services/<int:pk>', views.ServiceDetailView.as_view(), name='service-detail'),
    path('services/create', views.ServiceCreateView.as_view(), name='service-create'),
    path('services/<int:pk>/update', views.ServiceUpdateView.as_view(), name='service-update'),
    path('services/<int:pk>/delete', views.ServiceDeleteView.as_view(), name='service-delete'),

    # Categories url 
    path('category', views.CategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>', views.CategoryDetailView.as_view(), name='category-detail'),
    path('category/create', views.CategoryCreateView.as_view(), name='category-create'),
    path('category/<int:pk>/update', views.CategoryUpdateView.as_view(), name='category-update'),
    path('category/<int:pk>/delete', views.CategoryDeleteView.as_view(), name='category-delete'),

    # Articles url 
    path('article', views.ArticleListView.as_view(), name='article-list'),
    path('article/<int:pk>', views.ArticleDetailView.as_view(), name='article-detail'),
    path('article/create', views.ArticleCreateView.as_view(), name='article-create'),
    path('article/<int:pk>/update', views.ArticleUpdateView.as_view(), name='article-update'),
    path('article/<int:pk>/delete', views.ArticleDeleteView.as_view(), name='article-delete'),

    # Progrmas url 
    path('program', views.ProgramListView.as_view(), name='program-list'),
    path('program/<int:pk>', views.ProgramDetailView.as_view(), name='program-detail'),
    path('program/create', views.ProgramCreateView.as_view(), name='program-create'),
    path('program/<int:pk>/update', views.ProgramUpdateView.as_view(), name='program-update'),
    path('program/<int:pk>/delete', views.ProgramDeleteView.as_view(), name='program-delete'),

    # Users url 
    path('user', views.UserListView.as_view(), name='user-list'),
    path('user/<int:pk>', views.UserDetailView.as_view(), name='user-detail'),
    path('user/create', views.UserCreateView.as_view(), name='user-create'),
    path('user/created', views.UserCreatedView.as_view(), name='user-created'),
    path('user/verify', views.UserVerifyView.as_view(), name='user-verify'),
    path('user/<int:pk>/update', views.UserUpdateView.as_view(), name='user-update'),
    path('user/<int:pk>/delete', views.UserDeleteView.as_view(), name='user-delete'),
]
