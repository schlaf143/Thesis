from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import timedelta, datetime

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, default="Unassigned")

    # Add a reverse relationship to Employee
    def get_employees(self):
        return self.employees.all()  # Allows easy retrieval of employees in this department

    def __str__(self):
        return self.name



class Employee(models.Model):
    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Prefer not to Say'),
    ]

    ROLE_CHOICES = [
        ('Regular Employee', 'Regular Employee'),
        ('Department Head', 'Department Head'),
        ('Administrator', 'Administrator'),
    ]

    employee_id = models.AutoField(primary_key=True)  
    company_id = models.CharField(max_length=20, blank=False, unique=True)
    first_name = models.CharField(max_length=100, blank=False)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=False)
    sex = models.CharField(max_length=20, choices=SEX_CHOICES, blank=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Regular Employee', blank=False)

    # Change ManyToManyField to ForeignKey (One-to-Many relationship)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")

    contact_number = models.CharField(max_length=15, blank=False)
    date_employed = models.DateField()
    leave_credits = models.IntegerField(default=0, blank=False)

    user_account = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='employee')

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        db_table = 'employee_table'
        constraints = [
            models.CheckConstraint(
                check=models.Q(leave_credits__gte=0),
                name='positive_leave_credits',
            ),
        ]
    
    def __str__(self):
        return f"{self.company_id} - {self.first_name} {self.middle_name if self.middle_name else ''} {self.last_name}"


class EmployeeSchedule(models.Model):
    employee = models.OneToOneField('Employee', on_delete=models.CASCADE)

    monday_start = models.TimeField(null=True, blank=True)
    monday_end = models.TimeField(null=True, blank=True)
    tuesday_start = models.TimeField(null=True, blank=True)
    tuesday_end = models.TimeField(null=True, blank=True)
    wednesday_start = models.TimeField(null=True, blank=True)
    wednesday_end = models.TimeField(null=True, blank=True)
    thursday_start = models.TimeField(null=True, blank=True)
    thursday_end = models.TimeField(null=True, blank=True)
    friday_start = models.TimeField(null=True, blank=True)
    friday_end = models.TimeField(null=True, blank=True)
    saturday_start = models.TimeField(null=True, blank=True)
    saturday_end = models.TimeField(null=True, blank=True)
    sunday_start = models.TimeField(null=True, blank=True)
    sunday_end = models.TimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Employee Schedule"
        verbose_name_plural = "Employee Schedules"
        db_table = "employee_schedule_table"

    def clean(self):
        if EmployeeSchedule.objects.filter(employee=self.employee).exclude(pk=self.pk).exists():
            raise ValidationError(f"Employee {self.employee} already has a schedule.")

        days = [
            ("Monday", self.monday_start, self.monday_end),
            ("Tuesday", self.tuesday_start, self.tuesday_end),
            ("Wednesday", self.wednesday_start, self.wednesday_end),
            ("Thursday", self.thursday_start, self.thursday_end),
            ("Friday", self.friday_start, self.friday_end),
            ("Saturday", self.saturday_start, self.saturday_end),
            ("Sunday", self.sunday_start, self.sunday_end),
        ]

        working_days = 0
        rest_days = 0

        for day, start, end in days:
            if start and end:
                start_datetime = datetime.combine(datetime.today(), start)
                end_datetime = datetime.combine(datetime.today(), end)

                if start_datetime >= end_datetime:
                    end_datetime += timedelta(days=1)

                if start_datetime >= end_datetime:
                    raise ValidationError({f"{day.lower()}_start": f"{day}: Start time must be earlier than end time."})

                duration = (end_datetime - start_datetime).seconds / 3600

                if duration != 9:
                    raise ValidationError({f"{day.lower()}_start": f"{day}: The work shift must be exactly 9 hours."})

                working_days += 1
            elif start or end:
                raise ValidationError({f"{day.lower()}_start": f"{day}: Both start and end times must be provided, or neither."})
            else:
                rest_days += 1

        if rest_days < 1:
            raise ValidationError("Employee must have at least one rest day in the week.")
        if working_days < 5:
            raise ValidationError(f"Employee must have at least 5 working days, but only {working_days} are set.")

    def get_schedule_for_day(self, day):
        start = getattr(self, f"{day.lower()}_start")
        end = getattr(self, f"{day.lower()}_end")

        if start and end:
            if start >= end:
                end = (datetime.combine(datetime.today(), end) + timedelta(days=1)).time()
            return f"{day}: {start.strftime('%H:%M')} to {end.strftime('%H:%M')}"
        return f"{day}: Rest Day"

    def is_rest_day(self, day):
        return not getattr(self, f"{day.lower()}_start") and not getattr(self, f"{day.lower()}_end")

    def __str__(self):
        return f"Schedule for {self.employee}"
