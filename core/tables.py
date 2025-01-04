import django_tables2 as tables
from django.utils.html import format_html
from .models import Employee, EmployeeSchedule

class EmployeeHTMxTable(tables.Table):
    edit = tables.Column(empty_values=(), orderable=False, verbose_name='Actions')

    class Meta:
        model = Employee
        template_name = "htmx_template.html"
        exclude = ('employee_id', "sex", "date_employed")
        fields = (
            'company_id',  
            'first_name',
            'middle_name',
            'last_name',
            'role',
            'department',
            'contact_number',
            'leave_credits',
            'user_account',
            'edit',
        )
    def render_edit(self, record):
        return format_html(
            '<a href="/employee/edit/{}/" class="btn btn-sm btn-warning">Edit</a>',
            record.employee_id
        )
        
class EmployeeScheduleHTMxTable(tables.Table):
    edit = tables.Column(empty_values=(), orderable=False, verbose_name='Actions')
    employee_department = tables.Column(accessor='employee.department', verbose_name='Department')
    employee_company_id = tables.Column(accessor='employee.company_id', verbose_name='Company ID')

    class Meta:
        model = EmployeeSchedule
        template_name = "htmx_template.html"
        exclude = ('employee_id',)
        fields = (
            'employee', 
            'employee_company_id',
            'employee_department',
            'monday_start', 'monday_end',
            'tuesday_start', 'tuesday_end',
            'wednesday_start', 'wednesday_end',
            'thursday_start', 'thursday_end',
            'friday_start', 'friday_end',
            'saturday_start', 'saturday_end',
            'sunday_start', 'sunday_end',
            'edit',
        )
        attrs = {
            "class": "table table-bordered table-striped table-hover",
        }  # Apply Bootstrap styles

    def render_edit(self, record):
        return format_html(
            '<a href="/schedule/edit/{}/" class="btn btn-sm btn-warning htmx-trigger">Edit</a>',
            record.id 
        )
        
        #record.employee_id -> employee
        #record.id -> schedule
        #this is where the url takes the primary key and passese it