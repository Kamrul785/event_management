from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def no_permission(request):
    return render(request, 'no_permission.html')


def custom_404(request, exception):
    return render(request, '404.html', status=404)