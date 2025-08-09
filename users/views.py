from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import  Group, Permission
from users.forms import CustomRegistrationForm, LoginForm ,AssignRoleForm, CreateGroupForm, CustomPasswordChangeForm, CustomPasswordRestForm, CustomPasswordRestConfirmForm, EditProfileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test
from events.views import is_organizer, is_participant
from django.views.generic import TemplateView, UpdateView, CreateView, FormView, ListView
from django.contrib.auth.views import LoginView,PasswordChangeView, PasswordResetView , PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.

#test for user

def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def profile_view(request):
    return render(request,'profile.html')

def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            print('user', user)
            user.is_active = False
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful! Please check your email to activate your account.')
            return redirect('sign_in') 
        else:
            print("form are not valid")
    return render(request, 'registration/register.html', {'form':form})   

def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name} {user.last_name}!')
                return redirect('home') 
            else:
                messages.error(request, 'Please activate your account first. Check your email.')
    return render(request, 'registration/login.html', {'form':form})

@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('sign_in')
    return HttpResponse('login first to sign_out')
    
def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id = user_id)
        if default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been activated successfully")
            return redirect('sign_in')
        else:
            return HttpResponse('Invalid activation Link, Please try again!!')
    except User.DoesNotExist:
        messages.error(request,"User not found")
        return redirect('sign_in')
    
    
@user_passes_test(is_admin, login_url='no_permission')
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, 'admin/dashboard.html', {'users':users})


@user_passes_test(is_admin, login_url='no_permission')
def assign_role(request,user_id):
    user= User.objects.get(id = user_id)
    form = AssignRoleForm()
    if request.method == "POST":
        form = AssignRoleForm(request.POST)
        
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, 'Role changes successfully')
            return redirect('admin_dashboard')
    return render(request, 'admin/assign_role.html', {'form':form, 'user':user})


# def admin_dashboard(request):
#     users = User.objects.all()
#     return render(request, 'admin/dashboard.html', {'users': users})

# @login_required  
# def assign_role(request, user_id):
#     try:
#         user = User.objects.get(id=user_id)
#     except User.DoesNotExist:
#         messages.error(request, "User not found")
#         return redirect('admin_dashboard')
    
#     form = AssignRoleForm()
#     if request.method == "POST":
#         form = AssignRoleForm(request.POST)
#         if form.is_valid():  # Fixed missing parentheses
#             role = form.cleaned_data.get('role')
#             user.groups.clear()
#             user.groups.add(role)
#             messages.success(request, 'Role changed successfully')
#             return redirect('admin_dashboard')
#     return render(request, 'admin/assign_role.html', {'form': form, 'user': user})

@user_passes_test(is_admin, login_url='no_permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f'A group {group.name} created successfully')
            return redirect(create_group)
    
    return render(request, 'admin/create_group.html', {'form':form})


class CreateGroup(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Group
    template_name = 'admin/create_group.html'
    form_class = CreateGroupForm
    success_url = reverse_lazy('create_group')
    login_url = 'no_permission'
    
    def test_func(self):
        return is_admin(self.request.user)
    
    def form_valid(self, form):
        context =  super().form_valid(form)
        messages.success(self.request, f'A group {self.object.name} created successfully')

        return context
    

@login_required
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups':groups})

class GroupList(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Group
    context_object_name = 'groups'
    template_name = 'admin/group_list.html'
    login_url = 'no_permission'
    
    def test_func(self):
        return is_admin(self.request.user)
    
    def get_queryset(self):
        queryset = Group.objects.prefetch_related('permissions').all()
        return queryset


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['profile_image'] = user.profile_image
        context['phone_number'] = user.phone_number
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        
        return context 

class ChangePassword(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    form_class = CustomPasswordChangeForm


class CustomPasswordRestView(PasswordResetView):
    form_class = CustomPasswordRestForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign_in')
    html_email_template_name = 'registration/reset_email.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        print(context)
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'A password rest email sent.Please check your email')
        return super().form_valid(form)
    
class CustomPasswordRestConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordRestConfirmForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign_in')
    
    def form_valid(self, form):
        messages.success(self.request, 'Password Reset Successfully')
        return super().form_valid(form)
    


class EditProfileView(UpdateView):
    Model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self,form):
        form.save()
        return redirect('profile_view')



def dashboard(request):
    if is_admin(request.user):
        return redirect('admin_dashboard')
    elif is_organizer(request.user):
        return redirect('organizer_dashboard')
    elif is_participant(request.user):
        return redirect('participant_dashboard')
    
    return redirect('no_permission')