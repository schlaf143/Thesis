from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from datetime import timedelta, datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

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

    employee_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    company_id = models.CharField(max_length=20, blank=False)  # Changed to CharField
    first_name = models.CharField(max_length=100, blank=False)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=False)
    sex = models.CharField(max_length=20, choices=SEX_CHOICES, blank=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Regular Employee', blank=False)

    department = models.CharField(max_length=100, blank=False)
    contact_number = models.CharField(max_length=15, blank=False)
    date_employed = models.DateField()
    leave_credits = models.IntegerField(default=0, blank=False)

    # Foreign key linking the employee to a user account
    user_account = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='employee')

    class Meta:
        ordering = ['last_name', 'first_name']  # Default ordering
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        db_table = 'employee_table'  # Custom database table name
        constraints = [
            models.CheckConstraint(
                check=models.Q(leave_credits__gte=0),
                name='positive_leave_credits',
            ),
        ]
        
    def clean(self):
        # Validate contact number (must contain only digits and be at least 10 digits)
        if not self.contact_number.isdigit():
            raise ValidationError("Contact number must only contain digits.")
        if len(self.contact_number) < 10:
            raise ValidationError("Contact number must be at least 10 digits long.")

        # Validate leave credits (cannot be negative)
        if self.leave_credits < 0:
            raise ValidationError("Leave credits cannot be negative.")
        
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
        """Custom validations:
        1. Check if an employee has existing schedules
        2. Make sure that an employee has both start and end times (i.e. no employee
        has a start time but no end time and vice versa)
        3. Make sure that time between start and end is always 9 hours
        4. Ensure that an employee has atleast 5 working days and 1 rest day
        5. Make sure employee cannot have negative rest day"""
        
        # Check if an employee already has a schedule
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
                
        working_days = 0  # Counter for working days
        rest_days = 0     # Counter for rest days

        for day, start, end in days:
            if start and end:
                # Convert start and end times to datetime objects for proper comparison
                start_datetime = datetime.combine(datetime.today(), start)
                end_datetime = datetime.combine(datetime.today(), end)

                # Check if the shift spans midnight (end time is earlier than start time)
                if start_datetime >= end_datetime:
                    # Shift spans midnight, so adjust the end time by adding one day
                    end_datetime += timedelta(days=1)

                # Validate that the start time is earlier than the end time after adjusting for midnight shifts
                if start_datetime >= end_datetime:
                    raise ValidationError({f"{day.lower()}_start": f"{day}: Start time must be earlier than end time."})

                # Ensure the shift is exactly 9 hours
                duration = (end_datetime - start_datetime).seconds / 3600  # Duration in hours
                
                if duration != 9:
                    raise ValidationError({f"{day.lower()}_start": f"{day}: The work shift must be exactly 9 hours."})
                working_days += 1  # Increment the working days counter
            elif start or end:
                raise ValidationError({f"{day.lower()}_start": f"{day}: Both start and end times must be provided, or neither."})
            else:
                rest_days += 1  # Increment the rest days counter
        # Ensure the employee has at least 1 rest day
        if rest_days == 0:
            raise ValidationError("Employee must have at least one rest day in the week.")
        if rest_days < 1:
            raise ValidationError("Employee cannot have negative rest day in the week.")

        # Ensure the employee has at least 5 working days
        if working_days < 5:
            raise ValidationError(f"Employee must have at least 5 working days, but only {working_days} are set.")
    
    def get_schedule_for_day(self, day):
        """Return a formatted string for a specific day."""
        start = getattr(self, f"{day.lower()}_start")

        # Get the end time for the day
        
        end = getattr(self, f"{day.lower()}_end")
        if start and end:
            # Check if the end time is earlier than the start time (shift spans midnight)
            if start >= end:
                # Shift spans midnight, adjust the end time by adding 1 day
                end = (datetime.combine(datetime.today(), end) + timedelta(days=1)).time()
            return f"{day}: {start.strftime('%H:%M')} to {end.strftime('%H:%M')}"
        return f"{day}: Rest Day"

    def is_rest_day(self, day):
        start = getattr(self, f"{day.lower()}_start")
        end = getattr(self, f"{day.lower()}_end")
        return not start and not end

    def __str__(self):
        """String representation of the schedule."""
        return f"Schedule for {self.employee}"
