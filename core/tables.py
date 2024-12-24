# products/tables.py
import django_tables2 as tables
from .models import Employee

class EmployeeHTMxTable(tables.Table):
    class Meta:
        model = Employee
        template_name = "htmx_template.html"