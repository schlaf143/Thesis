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
    full_name = tables.Column(empty_values=(), orderable=False, verbose_name='FULL NAME')
    view = tables.Column(empty_values=(), orderable=True, verbose_name='ACTIONS')

    class Meta:
        model = Employee
        template_name = "htmx_template.html"
        exclude = ('employee_id', "sex", "date_employed", "first_name", "middle_name", "last_name",'leave_credits',)
        fields = (
            'company_id',
            'full_name', 
            'role',
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