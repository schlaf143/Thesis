import django_tables2 as tables
from django.utils.html import format_html
from .models import Employee, EmployeeSchedule

class EmployeeHTMxTable(tables.Table):
    edit = tables.Column(empty_values=(), orderable=True, verbose_name='ACTIONS')

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
        # Add Bootstrap table classes and custom attributes
        attrs = {
            "class": "table table-bordered table-hover",  # Adds Bootstrap table borders and hover effect
            "thead": {
                "class": "table-dark text-center text-uppercase", # Centers header text and adds dark background
            },
            "td": {
                "class": "text-center",  # Centers table data cell content
            },
            "th": {
                "class": "text-center",  # Centers table header cell content
            }
        }
    def render_edit(self, record):
        return format_html(
            '<a href="/employee/edit/{}/" class="btn btn-sm btn-warning me-1">Edit</a>',
            record.employee_id
        )


class EmployeeScheduleHTMxTable(tables.Table):
    # Combined time columns
    monday = tables.Column(verbose_name='Monday', accessor='monday_start')
    tuesday = tables.Column(verbose_name='Tuesday', accessor='tuesday_start')
    wednesday = tables.Column(verbose_name='Wednesday', accessor='wednesday_start')
    thursday = tables.Column(verbose_name='Thursday', accessor='thursday_start')
    friday = tables.Column(verbose_name='Friday', accessor='friday_start')
    saturday = tables.Column(verbose_name='Saturday', accessor='saturday_start')
    sunday = tables.Column(verbose_name='Sunday', accessor='sunday_start')
    
    edit = tables.Column(empty_values=(), orderable=True, verbose_name='Actions')
    employee_department = tables.Column(accessor='employee.department', verbose_name='Department')
    employee_company_id = tables.Column(accessor='employee.company_id', verbose_name='Company ID')

    class Meta:
        model = EmployeeSchedule
        template_name = "htmx_template.html"
        exclude = ('employee_id', 
                  'monday_start', 'monday_end',
                  'tuesday_start', 'tuesday_end',
                  'wednesday_start', 'wednesday_end',
                  'thursday_start', 'thursday_end',
                  'friday_start', 'friday_end',
                  'saturday_start', 'saturday_end',
                  'sunday_start', 'sunday_end')
        fields = (
            'employee', 
            'employee_company_id',
            'employee_department',
            'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday', 'sunday',
            'edit',
        )
        attrs = {
            "class": "table table-bordered table-hover",
            "thead": {"class": "table-dark text-center text-uppercase"},
            "td": {"class": "text-center"},
            "th": {"class": "text-center"}
        }

    def render_monday(self, record):
        return self._format_time_pair(record.monday_start, record.monday_end)

    def render_tuesday(self, record):
        return self._format_time_pair(record.tuesday_start, record.tuesday_end)

    # Add similar methods for other days
    def render_wednesday(self, record):
        return self._format_time_pair(record.wednesday_start, record.wednesday_end)

    def render_thursday(self, record):
        return self._format_time_pair(record.thursday_start, record.thursday_end)

    def render_friday(self, record):
        return self._format_time_pair(record.friday_start, record.friday_end)

    def render_saturday(self, record):
        return self._format_time_pair(record.saturday_start, record.saturday_end)

    def render_sunday(self, record):
        return self._format_time_pair(record.sunday_start, record.sunday_end)

    def _format_time_pair(self, start_time, end_time):
        if start_time and end_time != None:
            return format_html(
                '<span class="time-slot">{} - {}</span>',
                start_time.strftime("%I:%M %p"),
                end_time.strftime("%I:%M %p")
            )
        return  format_html(
            '<span class="time-slot>Off</span>',
        )

    def render_edit(self, record):
        return format_html(
            '<a href="/schedule/edit/{}/" class="btn btn-sm btn-warning">Edit</a>',
            record.id
        )

#record.employee_id -> employee
#record.id -> schedule
#this is where the url takes the primary key and passese it