from django.urls import path 
from events.views import test, event_list, event_detail, event_create, event_update, event_delete

urlpatterns = [
    path('test/', test),
    path('event_list/',event_list, name = "event_list"),
    path('event_detail/<int:id>/',event_detail, name = "event_detail"),
    path('event_create/',event_create, name = "event_create"),
    path('event_update/<int:id>',event_update, name = "event_update"),
    path('event_delete/<int:id>',event_delete, name = "event_delete"),
    
]
