from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import models
from . import forms
from django.views.generic import TemplateView, ListView, DetailView
from .lib.email_services import send_email
# Create your views here.
def index(request):
    services =  models.Service.objects.all()
    categories =  models.Category.objects.all()
    affiliates =  models.Affiliate.objects.filter(is_active = True)
    book_email = request.session.get('book_email')
    if(request.session.get('book_email')):
        del request.session['book_email']
    context = {
        "services": services,
        "categories": categories,
        "affiliates": affiliates,
        "book_email": book_email
    }
    return render(request, "index.html", context)


def confirm_signup(request):
    context = {
        "message": ""
    }
    otp = request.GET.get('otp', None)
    email = request.GET.get('email', None)
    if otp and email:
        try:
            valid = models.OTP.objects.get(email__iexact=email, number=otp)
            if valid:
                user = models.User.objects.get(email__iexact = valid.email)
                if(user):
                    user.is_active = True
                    user.save()
                context["message"] = "Your account has been confirmed!"
                valid.delete()
        except models.OTP.DoesNotExist:
            context["message"] = "This link has expired or is invalid"
    else:
        context["message"] = "This link has expired or is invalid"
    return render(request, "confirm_signup.html", context)


@login_required
def Logout(request):
    messages.success(request, "Succesfully logged out.")
    logout(request)
    return redirect('core:login')

def Login(request):
    
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin:index')
        return redirect('client:index')
    context= {
        'form': forms.LoginForm(request)
    }
    if request.method == 'POST':
        context['form'] = forms.LoginForm(request, request.POST)
        if context['form'].is_valid():
            messages.success(request, "Welcome back  "+str(request.user))
            if "next" in request.GET:
                to =request.GET["next"]
                return redirect(to)
            if request.user.is_superuser:
                return redirect('admin:index')
            return redirect('client:index')
        
    return render( request, 'login.html', context)


class AboutUsView(TemplateView):
    template_name = "about-us.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch services with covers
        services_with_covers = models.Service.objects.filter(cover__isnull=False)
        # Limit to 4 items
        covers = services_with_covers if services_with_covers.count() < 4 else services_with_covers[:4]
        # Add covers to the context
        context["covers"] = covers
        
        return context


class BlogListView(ListView):
    model = models.Article
    template_name = "blog/list.html"

class BlogDetailView(DetailView):
    model = models.Article
    template_name = "blog/blog.html"

class EventListView(ListView):
    model = models.Event
    template_name = "event/list.html"

class EventDetailView(DetailView):
    model = models.Event
    template_name = "event/detail.html"



class ServiceListView(TemplateView):
    template_name = "service/list.html"
    def  get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = models.Category.objects.filter(is_active = True).order_by('name')
        # Fetch services with covers
        services_with_covers = categories.filter(cover__isnull=False)
        # Limit to 4 items
        covers = services_with_covers if services_with_covers.count() < 4 else services_with_covers[:4]
        # Add covers to the context
        context["covers"] = covers
        context["category_list"] = categories
        
        return context


class ServiceDetailView(DetailView):
    model = models.Category
    template_name = "service/detail.html"


class CategoryListView(ListView):
    model = models.Category
    template_name = "industry/list.html"

class CategoryDetailView(DetailView):
    model = models.Category
    template_name = "industry/detail.html"
    


# team and affliates 
class TeamView(TemplateView):
    template_name = "team.html"
    def  get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        affiliates = models.Affiliate.objects.filter(is_active = True)
        context["affiliates"] = affiliates
        members = models.Member.objects.filter(is_active = True)
        context["members"] = members
        
        return context
    
from django.conf import settings
def book_meeting(request):
    if request.method == 'POST' and request.POST.get('email'):
        email = request.POST.get('email')
        request.session['book_email'] = email
        member = settings.CONSULTANT_EMAIL
        member_name = settings.CONSULTANT_NAME
        send_email(
            recipient= member, 
            subject= "Consultation Request", 
            template_name="email/consultation.html",
            context={
                "member": member_name,
                "email": email
            }
        )
    return redirect('core:landing')