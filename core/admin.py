from datetime import time
from django import forms
from django.contrib import admin
from django.forms.widgets import TextInput
from django.templatetags.static import static
from .models import Employee, EmployeeSchedule, Department  # Ensure Department is imported

class EmployeeAdmin(admin.ModelAdmin):
    # Display all columns in the list view of the admin panel
    list_display = (
        'employee_id', 'company_id', 'first_name', 'middle_name', 'last_name', 
        'sex', 'role', 'department', 'contact_number', 'date_employed', 'leave_credits', 'user_account'
    )
    
    # Add filtering options
    list_filter = ('role', 'sex', 'department', 'date_employed')  # Change 'departments' → 'department'

    # Enable search functionality
    search_fields = ('first_name', 'last_name', 'company_id', 'employee_id')

    # Add pagination
    list_per_page = 20

    # Define the fields in the form view
    fields = (
        'employee_id', 'company_id', 'first_name', 'middle_name', 'last_name', 
        'sex', 'role', 'department', 'contact_number', 'date_employed', 'leave_credits'
    )

    # Read-only fields
    readonly_fields = ('employee_id',)

class EmployeeScheduleAdminForm(forms.ModelForm):
    class Meta:
        model = EmployeeSchedule
        fields = '__all__'
    
    time_widget = forms.TimeField(
        required=False, 
        widget=TextInput(attrs={'class': 'flatpickr', 'data-time_24hr': 'false', 'data-date_format': 'h:i K'})
    )

    # Apply Flatpickr to time fields
    monday_start = time_widget
    monday_end = time_widget
    tuesday_start = time_widget
    tuesday_end = time_widget
    wednesday_start = time_widget
    wednesday_end = time_widget
    thursday_start = time_widget
    thursday_end = time_widget
    friday_start = time_widget
    friday_end = time_widget
    saturday_start = time_widget
    saturday_end = time_widget
    sunday_start = time_widget
    sunday_end = time_widget

class EmployeeScheduleAdmin(admin.ModelAdmin):
    form = EmployeeScheduleAdminForm

    # Fields to display in the list view
    list_display = (
        'id', 'employee', 'monday_start', 'monday_end', 'tuesday_start', 'tuesday_end', 
        'wednesday_start', 'wednesday_end', 'thursday_start', 'thursday_end', 
        'friday_start', 'friday_end', 'saturday_start', 'saturday_end', 
        'sunday_start', 'sunday_end'
    )
    
    # Enable search for employees
    search_fields = ('employee__first_name', 'employee__last_name')

    # Fix: Use 'employee__department' instead of 'employee__departments' in filtering
    list_filter = ('employee__department',)

    class Media:
        # Reference static files
        js = (static('js/flatpickr.js'), static('js/flatpickr_init.js'))
        css = {'all': (static('css/flatpickr.min.css'),)}


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeSchedule, EmployeeScheduleAdmin)
admin.site.register(Department) 
