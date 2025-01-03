from decimal import Decimal
from django.db.models import Q
from django.forms import TextInput
import django_filters
from .models import Employee, EmployeeSchedule

class EmployeeFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(
        method='universal_search',
        label="",
        widget=TextInput(attrs={'placeholder' : 'Search with Company ID, Name, Role, or Department'}))
    
    class Meta:
        model = Employee
        fields = ['query']

    
    def universal_search(self, queryset, name, value):
        #Search
        if value.replace(".", "", 1).isdigit():
            # If the value is a number (like an employee_id or leave credits), filter by ID or leave credits
            return queryset.filter(
                Q(employee_id=value) | Q(leave_credits=value)
            )
        # Default search by first_name, last_name, department, and role
        return queryset.filter(
            Q(company_id__icontains=value) |
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(middle_name__icontains=value) |
            Q(department__icontains=value) |
            Q(role__icontains=value)
        )
        
class EmployeeScheduleFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(
        method='universal_search', 
        label="", 
        widget=TextInput(attrs={'placeholder': 'Search by Employee Name or Department'})
    )

    class Meta:
        model = EmployeeSchedule
        fields = ['query']

    def universal_search(self, queryset, name, value):
        #Search
        return queryset.filter(
            Q(employee__first_name__icontains=value) |  
            Q(employee__middle_name__icontains=value) |  
            Q(employee__last_name__icontains=value) | 
            Q(employee__company_id__icontains=value) |   
            Q(employee__department__icontains=value) 
        )
        