import django_tables2 as tables
from django.utils.html import format_html
from .models import Employee, EmployeeSchedule

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

class EmployeeScheduleTable(tables.Table):
    employee_name = tables.Column(verbose_name="Employee Name")
    department = tables.Column(verbose_name="Department")

    monday = tables.Column(verbose_name="Monday")
    tuesday = tables.Column(verbose_name="Tuesday")
    wednesday = tables.Column(verbose_name="Wednesday")
    thursday = tables.Column(verbose_name="Thursday")
    friday = tables.Column(verbose_name="Friday")
    saturday = tables.Column(verbose_name="Saturday")
    sunday = tables.Column(verbose_name="Sunday")

    edit = tables.Column(empty_values=(), orderable=False, verbose_name='Actions')
    
    class Meta:
        model = EmployeeSchedule
        template_name = "htmx_template.html"
        exclude = ('employee_id',)

    def render_employee_name(self, record):
        # Combine first name, middle name, and last name
        employee = record.employee
        return f"{employee.first_name} {employee.middle_name or ''} {employee.last_name}".strip()

    def render_department(self, record):
        return record.employee.department.name if record.employee.department else "N/A"

    def render_monday(self, record):
        return record.get_schedule_for_day("Monday")

    def render_tuesday(self, record):
        return record.get_schedule_for_day("Tuesday")

    def render_wednesday(self, record):
        return record.get_schedule_for_day("Wednesday")

    def render_thursday(self, record):
        return record.get_schedule_for_day("Thursday")

    def render_friday(self, record):
        return record.get_schedule_for_day("Friday")

    def render_saturday(self, record):
        return record.get_schedule_for_day("Saturday")

    def render_sunday(self, record):
        return record.get_schedule_for_day("Sunday")
    # Repeat for other days (Wednesday, Thursday, etc.)

"""     def render_edit(self, record):
        # Edit button
        return format_html(
            '<a href="/employee_schedule/edit/{}/" class="btn btn-sm btn-warning">Edit</a>',
            record.id
        ) """