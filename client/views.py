from django.shortcuts import render

# Create your views here.

def IndexView(request):
    return render(request, "client/index.html")

def BusinessesView(request):
    context = {}
    if request.method == "POST":
        state_value = request.POST.get('state')
        context['state'] = state_value
    return render(request, "client/businesses.html", context)