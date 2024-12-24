from decimal import Decimal
from django.db.models import Q
import django_filters
from .models import Employee

class EmployeeFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search', label="Search")
    first_name = django_filters.CharFilter(lookup_expr='icontains', label='First Name')
    last_name = django_filters.CharFilter(lookup_expr='icontains', label='Last Name')
    department = django_filters.CharFilter(lookup_expr='icontains', label='Department')
    role = django_filters.ChoiceFilter(choices=Employee.ROLE_CHOICES, label='Role')
    sex = django_filters.ChoiceFilter(choices=Employee.SEX_CHOICES, label='Sex')
    employee_id = django_filters.NumberFilter(lookup_expr='exact', label='Employee ID')
    leave_credits = django_filters.NumberFilter(lookup_expr='gte', label='Leave Credits')

    class Meta:
        model = Employee
        fields = ['query', 'first_name', 'last_name', 'department', 'role', 'sex', 'employee_id', 'leave_credits']

    def universal_search(self, queryset, name, value):
        """
        Custom method to allow searching across multiple fields.
        """
        if value.replace(".", "", 1).isdigit():
            # If the value is a number (like an employee_id or leave credits), filter by ID or leave credits
            return queryset.filter(
                Q(employee_id=value) | Q(leave_credits=value)
            )
        # Default search by first_name, last_name, department, and role
        return queryset.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(department__icontains=value) |
            Q(role__icontains=value)
        )
