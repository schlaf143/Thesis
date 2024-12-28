import django_tables2 as tables
from django.utils.html import format_html
from .models import Employee

class EmployeeHTMxTable(tables.Table):
    edit = tables.Column(empty_values=(), orderable=False, verbose_name='Actions')

    class Meta:
        model = Employee
        template_name = "htmx_template.html"
        exclude = ('employee_id',)
        
    def render_edit(self, record):
        return format_html(
            '<a href="/employee/edit/{}/" class="btn btn-sm btn-warning">Edit</a>',
            record.employee_id
        )
