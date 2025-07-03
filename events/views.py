from django.shortcuts import render,redirect
from django.http import HttpResponse
from events.models import Category,Event,Participant
from events.forms import CategoryModelForm, EventModelForm, participantModelForm
from datetime import date
from django.db.models import Q , Min,Max,Count
from django.contrib import messages

def test(request):
    context = {
        "names" : ["Kamrul" , "Hasan" , "Sakil" , "Uddin"],
        "age" : 23 
    }
    return render(request, 'test.html' , context)

def event_list(request):
    events = Event.objects.select_related('category').all()
    context = {'events': events}
    return render(request, 'event_list.html' , context )

def event_detail(request, id):
    event = Event.objects.get(id = id)
    
    return render(request, 'event_detail.html', {'event':event})

def event_create(request):
    event_form = EventModelForm()
    
    if request.method == "POST":
        event_form = EventModelForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Created Successfully")
            redirect('event_list')
        
    return render(request, 'event_form.html', {'event_form': event_form})


def event_update(request,id):
    event = Event.objects.get(id=id)
    event_form = EventModelForm()
    
    if request.method == "POST":
        event_form = EventModelForm(request.POST, instance = event)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Updated Successfully")
            return redirect('event_list')
        
    return render(request, 'event_form.html', {'event_form' : event_form})

        
def event_delete(request,id):
    if request.method == "POST":
        event = Event.objects.get(id = id)
        event.delete()
        messages.success(request, "Event Deleted Successfully")
        return redirect('event_list')
    else:
        messages.error(request,"Something Went Wrong")
        return redirect('event_list')
