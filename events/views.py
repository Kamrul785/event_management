from django.shortcuts import render,redirect
from django.http import HttpResponse
from events.models import Category,Event,Participant
from events.forms import CategoryModelForm, EventModelForm, participantModelForm, EventFilterForm
from datetime import date
from django.db.models import Q , Min,Max,Count
from django.contrib import messages

def test(request):
    context = {
        "names" : ["Kamrul" , "Hasan" , "Sakil" , "Uddin"],
        "age" : 23 
    }
    return render(request, 'test.html' , context)

def home(request):
    search_item = request.GET.get('search', '')  
    events = Event.objects.all()
    if search_item:
        events = events.filter(
            Q(name__icontains=search_item) | Q(location__icontains=search_item) 
        )
    context = {
        'events': events,
        'search_item': search_item
    }
    return render(request, 'home.html', context)

def dashboard(request):
    
    type = request.GET.get('type','all')
    
    counts  = Event.objects.aggregate( 
        total_events = Count('id'),
        upcoming_events=Count('id', filter=Q(date__gte=date.today())),
        past_events=Count('id', filter=Q(date__lt=date.today())), 
    )
    total_participants = Participant.objects.count()
    today_events = Event.objects.filter(date = date.today())
    
    if type == 'upcoming':
        events = Event.objects.filter(date__gte= date.today()).annotate(num_participant=Count('participants')).all()
    elif type == 'past':
        events = Event.objects.filter(date__lt= date.today()).annotate(num_participant=Count('participants')).all()
    else:
        events = Event.objects.all().annotate(num_participant=Count('participants')).all()
    
    context = {
        'counts' : counts,
        'total_participants': total_participants,
        'today_events': today_events,
        'events': events,
        'type' : type
    }
    
    return render(request, 'dashboard.html', context)

def event_list(request):
    events = Event.objects.select_related('category').annotate(num_participant=Count('participants')).all()
    filter_form = EventFilterForm(request.GET)
    
    if filter_form.is_valid():
        category = filter_form.cleaned_data.get('category')
        start_date = filter_form.cleaned_data.get('start_date')
        end_date = filter_form.cleaned_data.get('end_date')
        
        if category:
            events = events.filter(category=category)
        if start_date:
            events = events.filter(date__gte=start_date)
        if end_date:
            events = events.filter(date__lte=end_date)
            
    total_participants = Participant.objects.count()

    context = {
        'events': events, 
        'total_participants':total_participants,
        'filter_form' : filter_form
    }
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
            return redirect('event_list')
        
    return render(request, 'event_form.html', {'event_form': event_form})

def event_update(request,id):
    event = Event.objects.get(id=id)
    event_form = EventModelForm(instance = event)
    
    if request.method == "POST":
        event_form = EventModelForm(request.POST, instance = event)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Updated Successfully")
        
    return render(request, 'event_form.html', {'event_form' : event_form , 'event' : event})
        
def event_delete(request,id):
    if request.method == "POST":
        event = Event.objects.get(id = id)
        event.delete()
        messages.success(request, "Event Deleted Successfully")
        return redirect('event_list')
    else:
        messages.error(request,"Event not deleted")
        return redirect('event_list')

def participant_list(request):
    participants = Participant.objects.annotate(num_event=Count('event')).all()
    context = {'participants': participants}
    return render(request, 'participant_list.html', context)

def participant_create(request):
    participant_form = participantModelForm()
    
    if request.method == "POST":
        participant_form = participantModelForm(request.POST)
        if participant_form.is_valid():
            participant_form.save()
            messages.success(request, "Participant Created Successfully")
            return redirect('participant_list') 
    
    return render(request, 'participant_form.html', {'participant_form': participant_form})

def participant_update(request, id):
    participant = Participant.objects.get(id=id)
    participant_form = participantModelForm(instance=participant)
    
    if request.method == "POST":
        participant_form = participantModelForm(request.POST, instance=participant)
        if participant_form.is_valid():
            participant_form.save()
            messages.success(request, "Participant Updated Successfully")
            return redirect('participant_list')
    
    return render(request, 'participant_form.html', {'participant_form': participant_form})

def participant_delete(request, id):    
    if request.method == "POST":
        participant = Participant.objects.get(id=id)
        participant.delete()
        messages.success(request, "Participant Deleted Successfully")
        return redirect('participant_list')
    else:
        messages.error(request,"Something Went Wrong")
        return redirect('participant_list')

def category_list(request):
    categories = Category.objects.all()
    
    return render(request, 'category_list.html', {'categories' : categories})

def category_create(request):
    category_form = CategoryModelForm()
    
    if request.method == "POST":
        category_form = CategoryModelForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, 'Category Created Successfully')
            return redirect('category_list')
        
    return render(request, 'category_form.html', {'category_form' : category_form})

def category_update(request,id):
    category = Category.objects.get(id = id)
    category_form = CategoryModelForm(instance = category)
    
    if request.method == "POST":
        category_form = CategoryModelForm(request.POST, instance = category)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, 'Category updated Successfully')
            redirect('category_list')
        
    return render(request, 'category_form.html', {'category_form' : category_form})

def category_delete(request,id):
    category = Category.objects.get(id=id)
    if request.method == "POST" :
        category.delete()
        messages.success(request, "Category Deleted Successfully")
        return redirect('category_list')
    
    return render(request, 'category_confirm_delete.html', {'category': category})

