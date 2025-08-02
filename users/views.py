from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User, Group, Permission
from users.forms import CustomRegistrationForm, LoginForm ,AssignRoleForm, CreateGroupForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test
from events.views import is_organizer, is_participant
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


@login_required
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups':groups})


def dashboard(request):
    if is_admin(request.user):
        return redirect('admin_dashboard')
    elif is_organizer(request.user):
        return redirect('organizer_dashboard')
    elif is_participant(request.user):
        return redirect('participant_dashboard')
    
    return redirect('no_permission')