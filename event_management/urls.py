from django.contrib import admin
from django.urls import path,include
from core.views import (
    about,
    api_documentation,
    best_practices,
    contact,
    cookie_policy,
    custom_404,
    event_planning_guide,
    help_center,
    home,
    no_permission,
    privacy_policy,
    terms_of_service,
    video_tutorials,
)
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('help-center/', help_center, name='help_center'),
    path('api-documentation/', api_documentation, name='api_documentation'),
    path('event-planning-guide/', event_planning_guide, name='event_planning_guide'),
    path('best-practices/', best_practices, name='best_practices'),
    path('video-tutorials/', video_tutorials, name='video_tutorials'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('terms-of-service/', terms_of_service, name='terms_of_service'),
    path('cookie-policy/', cookie_policy, name='cookie_policy'),
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