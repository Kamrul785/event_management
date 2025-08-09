from django.shortcuts import render,redirect , get_object_or_404
from django.http import HttpResponse
from events.models import Category,Event
from events.forms import CategoryModelForm, EventModelForm, EventFilterForm
from datetime import date
from django.db.models import Q , Min,Max,Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test, permission_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.views.generic import TemplateView, UpdateView, CreateView, FormView, ListView , DetailView
from django.contrib.auth.views import LoginView,PasswordChangeView, PasswordResetView , PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model

User = get_user_model()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_participant(user):
    return user.groups.filter(name='Participant').exists()

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

@user_passes_test(is_organizer, login_url='no_permission')
def organizer_dashboard(request):
    
    type = request.GET.get('type','all')
    
    counts  = Event.objects.aggregate( 
        total_events = Count('id'),
        upcoming_events=Count('id', filter=Q(date__gte=date.today())),
        past_events=Count('id', filter=Q(date__lt=date.today())), 
    )
    total_participants = User.objects.count()
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
    
    return render(request, 'organizer_dashboard.html', context)

@user_passes_test(is_participant, login_url='no_permission')
def participant_dashboard(request):
    upcoming_events = request.user.event.filter(date__gte=date.today()).select_related('category')
    
    stats = {
        'total_rsvps': request.user.event.count(),
        'confirmed_rsvps': request.user.event.count(),
        'upcoming_events': upcoming_events.count(),
        'past_events': request.user.event.filter(date__lt=date.today()).count()
    }

    context = {
        'stats': stats,
        'user_role': 'Participant',
        'upcoming_events': [
            {
                'event': event,
                'response': 'Confirmed'
            } for event in upcoming_events
        ]
    }
    return render(request, 'participant_dashboard.html', context)


@login_required
@permission_required('events.view_event', login_url='no_permission')
def event_list(request):
    events = Event.objects.select_related('category').annotate(num_participant=Count('participants')).all()
    form = EventFilterForm(request.GET)
    
    if form.is_valid():
        category = form.cleaned_data.get('category')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        
        if category:
            events = events.filter(category=category)
        if start_date:
            events = events.filter(date__gte=start_date)
        if end_date:
            events = events.filter(date__lte=end_date)
            
    total_participants = User.objects.count()

    context = {
        'events': events, 
        'total_participants':total_participants,
        'form' : form
    }
    return render(request, 'event_list.html' , context )

class EventList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Event
    template_name = 'event_list.html'
    permission_required = 'events.view_event'
    login_url = 'no_permission'
    context_object_name = 'events'
    
    
    def get_queryset(self):
        queryset = Event.objects.select_related('category').annotate(num_participant=Count('participants')).all()
        form = EventFilterForm(self.request.GET)
        if form.is_valid():
            category = form.cleaned_data.get('category')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            
            if category:
                queryset = queryset.filter(category=category)
            if start_date:
                queryset = queryset.filter(date__gte=start_date)
            if end_date:
                queryset = queryset.filter(date__lte=end_date)
        
        return queryset

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EventFilterForm(self.request.GET)
        context['total_participants'] = User.objects.count()
        return context
    
    
    


@login_required
@permission_required('events.view_event', login_url='no_permission')
def event_detail(request, id):
    event = Event.objects.get(id = id)  
    return render(request, 'event_detail.html', {'event':event})

class EventDetail(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'
    permission_required = 'events.view_event'
    login_url = 'no_permission'
    pk_url_kwarg = 'id'
    

@login_required
@permission_required('events.add_event', login_url='no_permission')
def event_create(request):
    event_form = EventModelForm()
    
    if request.method == "POST":
        event_form = EventModelForm(request.POST, request.FILES)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Created Successfully")
            return redirect('event_list')
        
    return render(request, 'event_form.html', {'event_form': event_form})


class CreateEvent(LoginRequiredMixin,PermissionRequiredMixin,SuccessMessageMixin,CreateView):
    model = Event
    template_name = 'event_form.html'
    form_class = EventModelForm
    permission_required='events.add_event'
    login_url = 'no_permission'
    success_url = reverse_lazy('event_list')
    success_message = 'Event Created Successfully'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_form'] = context['form']
        return context
    


@login_required
@permission_required('events.change_event', login_url='no_permission')
def event_update(request,id):
    event = Event.objects.get(id=id)
    event_form = EventModelForm(instance = event)
    
    if request.method == "POST":
        event_form = EventModelForm(request.POST, instance = event)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Updated Successfully")
        
    return render(request, 'event_form.html', {'event_form' : event_form , 'event' : event})


@login_required
@permission_required('events.delete_event', login_url='no_permission')
def event_delete(request,id):
    if request.method == "POST":
        event = Event.objects.get(id = id)
        event.delete()
        messages.success(request, "Event Deleted Successfully")
        return redirect('event_list')
    else:
        messages.error(request,"Event not deleted")
        return redirect('event_list')


@login_required
@permission_required('events.view_participant', login_url='no_permission')
def participant_list(request):
    participants = User.objects.annotate(num_event=Count('event')).all()
    context = {'participants': participants}
    return render(request, 'participant_list.html', context)


@login_required
@permission_required('events.add_user', login_url='no_permission')
def participant_create(request):
    participant_form = UserCreationForm()
    
    if request.method == "POST":
        participant_form = UserCreationForm(request.POST)
        if participant_form.is_valid():
            participant_form.save()
            messages.success(request, "Participant Created Successfully")
            return redirect('participant_list') 
    
    return render(request, 'participant_form.html', {'participant_form': participant_form})


@login_required
@permission_required('events.change_participant', login_url='no_permission')
def participant_update(request, id):
    participant = User.objects.get(id=id)
    participant_form = UserChangeForm(instance=participant)
    
    if request.method == "POST":
        participant_form = UserChangeForm(request.POST, instance=participant)
        if participant_form.is_valid():
            participant_form.save()
            messages.success(request, "Participant Updated Successfully")
            return redirect('participant_list')
    
    return render(request, 'participant_form.html', {'participant_form': participant_form})


@login_required
@permission_required('events.delete_participant', login_url='no_permission')
def participant_delete(request, id):    
    if request.method == "POST":
        participant = User.objects.get(id=id)
        participant.delete()
        messages.success(request, "Participant Deleted Successfully")
        return redirect('participant_list')
    else:
        messages.error(request,"Something Went Wrong")
        return redirect('participant_list')


@login_required
@permission_required('events.view_category', login_url='no_permission')
def category_list(request):
    categories = Category.objects.all()
    
    return render(request, 'category_list.html', {'categories' : categories})


@login_required
@permission_required('events.add_category', login_url='no_permission')
def category_create(request):
    category_form = CategoryModelForm()
    
    if request.method == "POST":
        category_form = CategoryModelForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, 'Category Created Successfully')
            return redirect('category_list')
        
    return render(request, 'category_form.html', {'category_form' : category_form})


@login_required
@permission_required('events.change_category', login_url='no_permission')
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


@login_required
@permission_required('events.delete_category', login_url='no_permission')
def category_delete(request,id):
    category = Category.objects.get(id=id)
    if request.method == "POST" :
        category.delete()
        messages.success(request, "Category Deleted Successfully")
        return redirect('category_list')
    
    return render(request, 'category_confirm_delete.html', {'category': category})


def rsvp_event(request, id):
    event = Event.objects.get(id = id)
    
    if request.user in event.participants.all():
        messages.info(request, "You are already done RSVP to this event")
        
    else:
        event.participants.add(request.user)
        event.save()
        messages.success(request,f"You have RSVP'd to {event.name} successfully")
        
    return redirect('event_list')