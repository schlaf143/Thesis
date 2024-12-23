from django.contrib import admin
from .models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    # Display all columns in the list view of the admin panel
    list_display = (
        'employee_id', 'company_id', 'first_name', 'middle_name', 'last_name', 
        'sex', 'role', 'department', 'contact_number', 'date_employed', 'leave_credits'
    )
    
    # Optional: Add filtering options for more control
    list_filter = ('role', 'sex', 'department', 'date_employed')

    # Optional: Enable search functionality
    search_fields = ('first_name', 'last_name', 'company_id', 'employee_id')

    # Optional: Add pagination to manage large data more easily
    list_per_page = 20

    # Optional: Define the fields in the form view to control the display order
    fields = (
        'employee_id', 'company_id', 'first_name', 'middle_name', 'last_name', 
        'sex', 'role', 'department', 'contact_number', 'date_employed', 'leave_credits'
    )

    # Optional: Read-only fields (optional)
    readonly_fields = ('employee_id',)

# Register the Employee model and its admin configuration
admin.site.register(Employee, EmployeeAdmin)
