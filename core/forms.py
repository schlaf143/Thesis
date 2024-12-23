from django import forms
from .models import Employee
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'  # Include all fields from the model
        widgets = {
            'company_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company ID',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name',
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter middle name (optional)',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name',
            }),
            'sex': forms.Select(attrs={
                'class': 'form-control',
            }),
            'role': forms.Select(attrs={
                'class': 'form-control',
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter department',
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., +1234567890',
            }),
            'date_employed': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'leave_credits': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
        }

    def clean_contact_number(self):
        contact_number = self.cleaned_data['contact_number']
        if not contact_number.isdigit():
            raise forms.ValidationError("Contact number must only contain digits.")
        if len(contact_number) < 10:
            raise forms.ValidationError("Contact number must be at least 10 digits long.")
        return contact_number

    def clean_leave_credits(self):
        leave_credits = self.cleaned_data['leave_credits']
        if leave_credits < 0:
            raise forms.ValidationError("Leave credits cannot be negative.")
        return leave_credits