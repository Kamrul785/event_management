from django import forms 
from events.models import Event, Category, Participant

class StyledFormMixing:
    default_classes = "border-2 border-gray-300 shadow-md w-full rounded-lg focus:border-rose-300 focus:ring-rose-500 p-2"
    
    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': self.default_classes})

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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()