from django import forms
import re
from django.contrib.auth.models import Group, Permission
from events.forms import StyledFormMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

# class StyledFormMixin:
#     """Mixin to apply consistent styling to form fields"""
    
#     default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-orange-500 focus:ring-orange-500"

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.apply_styled_widgets()

#     def apply_styled_widgets(self):
#         for field_name, field in self.fields.items():
#             if isinstance(field.widget, forms.TextInput):
#                 field.widget.attrs.update({
#                     'class': self.default_classes,
#                     'placeholder': f"Enter {field.label.lower()}"
#                 })
#             elif isinstance(field.widget, forms.EmailInput):
#                 field.widget.attrs.update({
#                     'class': self.default_classes,
#                     'placeholder': f"Enter {field.label.lower()}"
#                 })
#             elif isinstance(field.widget, forms.PasswordInput):
#                 field.widget.attrs.update({
#                     'class': self.default_classes,
#                 })
#             else:
#                 field.widget.attrs.update({
#                     'class': self.default_classes,
#                 })


class CustomRegistrationForm(StyledFormMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User 
        fields = ['username', 'first_name', 'last_name' , 'password','confirm_password', 'email']
        
    def clean_password(self):
        password = self.cleaned_data.get('password')
        error = []
        if len(password) < 8:
            error.append('Password must be at least 8 character long')
        
        if not re.search(r'[A-Z]', password):
            error.append('Password must include at least one uppercase letter')
        
        if not re.search(r'[a-z]', password):
            error.append('Password must include at least one lowercaser latter')
        
        if not re.search(r'[0-9]', password):
            error.append('Password must include at least one number')
         
        if not re.search(r'[!@#$%^&*(){}]', password):
            error.append('Password must include at one specail character')
        
        if error : 
            raise forms.ValidationError(error)
        
        return password
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exits = User.objects.filter(email = email).exists()
        if email_exits:
            raise forms.ValidationError("Email Already Exits")
        return email 
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password :
            raise forms.ValidationError("Password do not match")
        return cleaned_data

        
class LoginForm(StyledFormMixin,AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
class AssignRoleForm(StyledFormMixin,forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label = 'Select a role'
    )
    
class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'border-2 border-gray-300 shadow-md mt-4 rounded-lg p-3'}),
        required=False,
        label = 'Assign Permissions'
    )
    
    class Meta:
        model = Group
        fields = ['name', 'permissions']
        

class CustomPasswordChangeForm(StyledFormMixin,PasswordChangeForm):
    pass

class CustomPasswordRestForm(StyledFormMixin, PasswordResetForm):
    pass

class CustomPasswordRestConfirmForm(StyledFormMixin, SetPasswordForm):
    pass


class EditProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'profile_image', 'phone_number']