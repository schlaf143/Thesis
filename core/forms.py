from django import forms
from .models import Employee, EmployeeSchedule, Department
from django.templatetags.static import static
from datetime import timedelta, datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    
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
                'placeholder': 'Set Time',
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
    
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label='', 
        max_length=254, 
        help_text='Required. Enter a valid email address.', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    username = forms.CharField(
        label='', 
        max_length=30, 
        help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    role = forms.CharField(
        label='', 
        widget=forms.HiddenInput(), 
        initial='Regular Employee'
    )
    is_staff = forms.BooleanField(
        required=False, 
        label="Is This user a Department Head?", 
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    is_superuser = forms.BooleanField(
        required=False, 
        label="Is This user a HR Manager?", 
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_superuser')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].help_text = 'Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['email'].help_text = 'Required. Enter a valid email address.'

        self.fields['role'].widget.attrs['class'] = 'form-control'
        self.fields['role'].widget.attrs['placeholder'] = 'Role'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = self.cleaned_data.get('is_staff', False)
        user.is_superuser = self.cleaned_data.get('is_superuser', False)

        if commit:
            user.save()
        return user

