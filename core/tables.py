from math import e
import django_tables2 as tables
from django.utils.html import format_html
from .models import Employee, EmployeeSchedule
import os
from django.conf import settings

class EmployeeHTMxTable(tables.Table):
    full_name = tables.Column(empty_values=(), orderable=False, verbose_name='FULL NAME')
    view = tables.Column(empty_values=(), orderable=True, verbose_name='ACTIONS')

    class Meta:
        model = Employee
        template_name = "htmx_template.html"
        exclude = ('employee_id', "sex", "date_employed", "first_name", "middle_name", "last_name",'leave_credits',)
        fields = (
            'company_id',
            'full_name',  # New combined column
            'role',
            'department',
            'contact_number',
            'user_account',
            'view',
        )
        attrs = {
            "class": "table table-bordered table-hover",
            "thead": {
                "class": "table-dark text-center text-uppercase",
            },
            "td": {
                "class": "text-center",
            },
            "th": {
                "class": "text-center",
            }
        }

    def render_full_name(self, record):
        # Handle empty middle names gracefully
        middle = f" {record.middle_name}" if record.middle_name else ""
        return format_html(
            '<span class="employee-name">{}{} {}</span>',
            record.first_name,
            middle,
            record.last_name
        )

    def render_view(self, record):
        return format_html(
            '<a href="/employee/view/{}/" class="btn btn-sm btn-warning me-1">View</a>',
            record.employee_id 
        )
        
class EmployeeScheduleHTMxTable(tables.Table):
    full_name = tables.Column(accessor='employee', orderable=True, verbose_name='FULL NAME')
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
            'full_name',
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
            record.employee_id
        )

    def render_full_name(self, record):
        middle = f"{record.employee.middle_name}" if record.employee.middle_name else ""
        return format_html(
            '<span class="employee-name">{} {} {}</span>',
            record.employee.first_name,
            middle,
            record.employee.last_name
        )
#record.employee_id -> employee
#record.id -> schedule
#this is where the url takes the primary key and passese it

class EmployeeFaceEmbeddingsHTMxTable(tables.Table):
    full_name = tables.Column(empty_values=(), orderable=True, verbose_name='FULL NAME')
    face_embeddings = tables.Column(empty_values=(), orderable=False, verbose_name="FACE EMBEDDINGS")
    edit = tables.Column(empty_values=(), orderable=False, verbose_name='ACTIONS')
    
    class Meta:
        model = Employee
        template_name = "htmx_template.html"
        exclude = ('employee_id', "sex", "date_employed", "first_name", "middle_name", "last_name")
        fields = (
            'company_id',
            'full_name',
            'department',
            'face_embeddings',
            'edit',
        )
        attrs = {
            "class": "table table-bordered table-hover",
            "thead": {
                "class": "table-dark text-center text-uppercase",
            },
            "td": {
                "class": "text-center",
            },
            "th": {
                "class": "text-center",
            }
        }

    def get_embedding_directory(self, record):
        #VERY CHARACTER STRICT
        middle = f"{record.middle_name}" if record.middle_name else ""
        name = f"{record.first_name} {middle} {record.last_name}"
        #print(f"Names: {name}")
        return os.path.join(
            settings.BASE_DIR,
            'core',
            'static',
            'registered_faces',
            f"{name}_{record.company_id}"
        )

    def render_face_embeddings(self, record):
        """Check if embeddings exist in directory"""
        embed_dir = self.get_embedding_directory(record)
        
        if os.path.exists(embed_dir) and len(os.listdir(embed_dir)) > 0:
            return format_html('<span class="text-success">Active</span>')
        return format_html('<span class="text-danger">Inactive</span>')

    def render_edit(self, record):
        """Only show edit button if embeddings exist"""
        embed_dir = self.get_embedding_directory(record)
        
        if os.path.exists(embed_dir) and len(os.listdir(embed_dir)) > 0:
            return format_html(
                '<a href="/employee/edit/{}/" class="btn btn-sm btn-warning me-1">Edit</a>',
                record.employee_id 
            )
        return "-"

    def render_full_name(self, record):
        middle = f"{record.middle_name}" if record.middle_name else ""
        return format_html(
            '<span class="employee-name">{} {} {}</span>',
            record.first_name,
            middle,
            record.last_name
        )