from django.contrib import admin
from django.urls import path,include
from core.views import no_permission, home, about, contact, custom_404
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('events/',include("events.urls")),
    path('users/',include("users.urls")),
    path('no_permission/', no_permission, name='no_permission')
] 

handler404 = 'core.views.custom_404'
 
if settings.DEBUG:
    try:
        from debug_toolbar.toolbar import debug_toolbar_urls
        urlpatterns += debug_toolbar_urls()
    except ImportError:
        pass
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)