from django.contrib import admin
from django.urls import path,include
from events import views
from debug_toolbar.toolbar import debug_toolbar_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('events/',include("events.urls") )
] + debug_toolbar_urls()
