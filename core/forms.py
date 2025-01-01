from django import forms
from .models import Employee, EmployeeSchedule
from django.templatetags.static import static
from datetime import timedelta, datetime

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'  # Include all fields from the model
        
    def clean(self):
        """Remove redundant validation in the form."""
        # Simply call the model's clean method to do the validation
        cleaned_data = super().clean()
        return cleaned_data
    
class EmployeeScheduleForm(forms.ModelForm):
    class Media:
        # Reference to the local static files using the static tag
        js = (static('js/flatpickr.js'), static('js/flatpickr_init.js'))  # Include Flatpickr JS from the static directory
        css = {
            'all': (static('css/flatpickr.min.css'),)  # Include Flatpickr CSS from the static directory
        }
    class Meta:
        model = EmployeeSchedule
        fields = [
            'employee', 'monday_start', 'monday_end',
            'tuesday_start', 'tuesday_end',
            'wednesday_start', 'wednesday_end',
            'thursday_start', 'thursday_end',
            'friday_start', 'friday_end',
            'saturday_start', 'saturday_end',
            'sunday_start', 'sunday_end',
        ]
        time_widget = forms.TimeInput(attrs={ 
                'class': 'flatpickr form-control',
                'placeholder': 'Select start time',
                'data-time_24hr': 'true',
                'autocomplete' : 'off',
            })
        widgets = {
        'employee': forms.Select(attrs={'class': 'form-control'}),
        'monday_start': time_widget,
        'monday_end': time_widget,
        'tuesday_start': time_widget,
        'tuesday_end': time_widget,
        'wednesday_start': time_widget,
        'wednesday_end': time_widget,
        'thursday_start': time_widget,
        'thursday_end': time_widget,
        'friday_start': time_widget,
        'friday_end': time_widget,
        'saturday_start': time_widget,
        'saturday_end': time_widget,
        'sunday_start': time_widget,
        'sunday_end': time_widget,
        }

    def clean(self):
        """Remove redundant validation in the form."""
        # Simply call the model's clean method to do the validation
        cleaned_data = super().clean()
        return cleaned_data