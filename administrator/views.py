from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from core.models import Service, Category, Article, User, Affiliate, Member
from django.urls import reverse_lazy
from .forms import ServiceForm, CategoryForm, ArticleForm, UserForm, UserCreationForm, UserTokenVerifyForm, NewUserForm, AffiliateForm, MemberForm
from core.lib.email_services import send_email

# Tables import 

from administrator.tables import services_table, categories_table, articles_table, users_table, affiliate_table, members_table

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin,TemplateView):
    template_name = "admin/index.html"



# categories 
class AffiliateListView(LoginRequiredMixin,SingleTableMixin, FilterView):
    table_class = affiliate_table.Table
    queryset = Affiliate.objects.all()
    template_name = 'admin/affiliate/list.html'
    filterset_class = affiliate_table.Filter
    paginate_by= 5

class AffiliateDetailView(LoginRequiredMixin,DetailView):
    model = Affiliate
    template_name = 'admin/affiliate/details.html'

class AffiliateCreateView(LoginRequiredMixin,CreateView):
    model = Affiliate
    form_class = AffiliateForm
    template_name = 'admin/affiliate/create.html'
    def get_success_url(self):
        return reverse_lazy('admin:affiliate-detail', kwargs={'pk': self.object.pk})

class AffiliateUpdateView(LoginRequiredMixin,UpdateView):
    model = Affiliate
    form_class = AffiliateForm
    template_name = 'admin/affiliate/edit.html'
    def get_success_url(self):
        return reverse_lazy('admin:affiliate-detail', kwargs={'pk': self.object.pk})

class AffiliateDeleteView(LoginRequiredMixin,DeleteView):
    model = Affiliate
    template_name = 'admin/affiliate/delete.html'
    success_url = reverse_lazy('admin:affiliate-list')


# categories 
class MemberListView(LoginRequiredMixin,SingleTableMixin, FilterView):
    table_class = members_table.Table
    queryset = Member.objects.all()
    template_name = 'admin/member/list.html'
    filterset_class = members_table.Filter
    paginate_by= 5

class MemberDetailView(LoginRequiredMixin,DetailView):
    model = Member
    template_name = 'admin/member/details.html'

class MemberCreateView(LoginRequiredMixin,CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'admin/member/create.html'
    def get_success_url(self):
        return reverse_lazy('admin:member-detail', kwargs={'pk': self.object.pk})

class MemberUpdateView(LoginRequiredMixin,UpdateView):
    model = Member
    form_class = MemberForm
    template_name = 'admin/member/edit.html'
    def get_success_url(self):
        return reverse_lazy('admin:member-detail', kwargs={'pk': self.object.pk})

class MemberDeleteView(LoginRequiredMixin,DeleteView):
    model = Member
    template_name = 'admin/member/delete.html'
    success_url = reverse_lazy('admin:member-list')

# categories 
class CategoryListView(LoginRequiredMixin,SingleTableMixin, FilterView):
    table_class = categories_table.Table
    queryset = Category.objects.all()
    template_name = 'admin/category/list.html'
    filterset_class = categories_table.Filter
    paginate_by= 5

class CategoryDetailView(LoginRequiredMixin,DetailView):
    model = Category
    template_name = 'admin/category/details.html'

class CategoryCreateView(LoginRequiredMixin,CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'admin/category/create.html'
    def get_success_url(self):
        return reverse_lazy('admin:category-detail', kwargs={'pk': self.object.pk})

class CategoryUpdateView(LoginRequiredMixin,UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'admin/category/edit.html'
    def get_success_url(self):
        return reverse_lazy('admin:category-detail', kwargs={'pk': self.object.pk})

class CategoryDeleteView(LoginRequiredMixin,DeleteView):
    model = Category
    template_name = 'admin/category/delete.html'
    success_url = reverse_lazy('admin:category-list')


# services 
class ServiceListView(LoginRequiredMixin,SingleTableMixin, FilterView):
    table_class = services_table.Table
    queryset = Service.objects.all()
    template_name = 'admin/services/list.html'
    filterset_class = services_table.Filter
    paginate_by= 10

class ServiceDetailView(LoginRequiredMixin,DetailView):
    model = Service
    template_name = 'admin/services/details.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"{self.object.name} - Administrator"
        return context

class ServiceCreateView(LoginRequiredMixin,CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'admin/services/create.html'
    success_url = reverse_lazy('admin:service-list')

class ServiceUpdateView(LoginRequiredMixin,UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'admin/services/edit.html'
    success_url = reverse_lazy('admin:service-list')

class ServiceDeleteView(LoginRequiredMixin,DeleteView):
    model = Service
    template_name = 'admin/services/delete.html'
    success_url = reverse_lazy('admin:service-list')


# articles 
class ArticleListView(LoginRequiredMixin,SingleTableMixin, FilterView):
    table_class = articles_table.Table
    queryset = Article.objects.all()
    template_name = 'admin/article/list.html'
    filterset_class = articles_table.Filter
    paginate_by= 10

class ArticleDetailView(LoginRequiredMixin,DetailView):
    model = Article
    template_name = 'admin/article/details.html'
    
class ArticleCreateView(LoginRequiredMixin,CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'admin/article/create.html'
    success_url = reverse_lazy('admin:article-list')

class ArticleUpdateView(LoginRequiredMixin,UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'admin/article/edit.html'
    success_url = reverse_lazy('admin:article-list')

class ArticleDeleteView(LoginRequiredMixin,DeleteView):
    model = Article
    template_name = 'admin/article/delete.html'
    success_url = reverse_lazy('admin:article-list')


# Users 
class UserListView(LoginRequiredMixin,SingleTableMixin, FilterView):
    table_class = users_table.Table
    queryset = User.objects.all()
    template_name = 'admin/users/list.html'
    filterset_class = users_table.Filter
    paginate_by= 10
    

class UserDetailView(LoginRequiredMixin,DetailView):
    model = User
    template_name = 'admin/users/details.html'
    
class UserCreateView(LoginRequiredMixin,CreateView):
    model = User
    form_class = NewUserForm
    template_name = 'admin/users/create.html'
    success_url = reverse_lazy('admin:user-list')

    def form_valid(self, form):
        form.save(commit=True)
        return super().form_valid(form)
    

# class UserCreateView(LoginRequiredMixin,FormView):
#     template_name = 'admin/users/create.html'
#     form_class = UserCreationForm

#     def get_success_url(self) -> str:
#         print(self)
#         return reverse_lazy('admin:user-verify') + '?'+'email=test'

#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

class UserVerifyView(LoginRequiredMixin,FormView):
    template_name = 'admin/users/verify.html'
    form_class =  UserTokenVerifyForm
    success_url = reverse_lazy('admin:user-created')

    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'email': self.request.GET.get('email'),
        })
        return initial
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class UserCreatedView(LoginRequiredMixin,TemplateView):
    template_name = 'admin/user/created.html'


class UserUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = UserForm
    template_name = 'admin/users/edit.html'
    success_url = reverse_lazy('admin:user-list')

class UserDeleteView(LoginRequiredMixin,DeleteView):
    model = User
    template_name = 'admin/users/delete.html'
    success_url = reverse_lazy('admin:user-list')
