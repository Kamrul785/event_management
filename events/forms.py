from django import forms 
from events.models import Event, Category, Participant

class StyledFormMixing:
    default_classes = "border-2 border-gray-300 shadow-md w-full rounded-lg focus:border-rose-300 focus:ring-rose-500 p-2"
    
    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes}",
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class' : "border-2 border-gray-300 shadow-md rounded-lg focus:border-rose-300 focus:ring-rose-500 px-3 h-10"
                })
            elif isinstance(field.widget,forms.EmailInput):
                field.widget.attrs.update({
                    'class' : f"{self.default_classes}", 
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.CharField):
                field.widget.attrs.update({
                    'class' : "bg-gray-500"  
                })
            
class CategoryModelForm(StyledFormMixing,forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
        
class EventModelForm(StyledFormMixing,forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','description','date','time','location','category']
        widgets = {
            'date' : forms.SelectDateWidget,
            'time' : forms.TimeInput(attrs={'type' : 'time'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
        
class participantModelForm(StyledFormMixing,forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name','email','event']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'border-2 border-gray-300 shadow-md w-full rounded-lg p-2'}),
            'event': forms.CheckboxSelectMultiple(attrs={'class': 'border-2 border-gray-300 shadow-md mt-4 rounded-lg p-3'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
        
class EventFilterForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label="All Categories")
    start_date = forms.DateField(widget=forms.SelectDateWidget, required=False)
    end_date = forms.DateField(widget=forms.SelectDateWidget, required=False)