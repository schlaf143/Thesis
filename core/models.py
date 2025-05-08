from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import timedelta, datetime
from django.utils import timezone
from django.db.models import Max
from django.core.validators import MaxValueValidator
import pytz


class LeaveRequest(models.Model):
    class LeaveType(models.TextChoices):
        SICK = 'SICK', 'Sick Leave'
        MATERNITY = 'MATERNITY', 'Maternity Leave'
        PATERNITY = 'PATERNITY', 'Paternity Leave'
        VACATION = 'VACATION', 'Vacation Leave'

    class ApprovalStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='leave_requests')
    leave_number = models.PositiveIntegerField(unique=True, editable=False)
    start_of_leave = models.DateField()
    end_of_leave = models.DateField()
    reason_for_leave = models.TextField()
    leave_type = models.CharField(max_length=20, choices=LeaveType.choices)

    department_approval = models.CharField(max_length=10, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING)
    hr_approval = models.CharField(max_length=10, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING)
    president_approval = models.CharField(max_length=10, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING)
    status = models.CharField(max_length=10, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-generate leave number
        if not self.leave_number:
            max_leave_number = LeaveRequest.objects.aggregate(Max('leave_number'))['leave_number__max'] or 0
            self.leave_number = max_leave_number + 1

        # Optionally: Validate that start date is before end date
        if self.start_of_leave > self.end_of_leave:
            raise ValidationError("Start of leave must be before end of leave.")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Leave {self.leave_number} - {self.employee}"

class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)

    leave_respondents = models.ManyToManyField(
        'Employee',
        related_name='leave_departments',
        blank=True,
        limit_choices_to={'department__isnull': False}
    )
    shift_respondents = models.ManyToManyField(
        'Employee',
        related_name='shift_departments',
        blank=True,
        limit_choices_to={'department__isnull': False}
    )

    def __str__(self):
        return self.name

    def get_leave_respondents(self):
        return ", ".join([str(emp) for emp in self.leave_respondents.all()]) if self.leave_respondents.exists() else "Unassigned"

    def get_shift_respondents(self):
        return ", ".join([str(emp) for emp in self.shift_respondents.all()]) if self.shift_respondents.exists() else "Unassigned"


class Employee(models.Model):
    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Prefer not to Say'),
    ]

    ROLE_CHOICES = [
        ('Regular Employee', 'Regular Employee'),
        ('Department Head', 'Department Head'),
        ('Admin(HR)', 'Admin(HR)'),
        ('Supervisor', 'Supervisor'),
        ('President', 'President')
    ]

    employee_id = models.AutoField(primary_key=True)
    company_id = models.CharField(max_length=20, blank=False, unique=True)
    first_name = models.CharField(max_length=100, blank=False)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=False)
    sex = models.CharField(max_length=20, choices=SEX_CHOICES, blank=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Regular Employee', blank=False)

    department = models.ForeignKey(
        Department,
        related_name="employees",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

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

    def clean(self):
        if not self.contact_number.isdigit():
            raise ValidationError("Contact number must only contain digits.")
        if len(self.contact_number) < 10:
            raise ValidationError("Contact number must be at least 10 digits long.")

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

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('On-Time', 'On-Time'),
        ('Late', 'Late'),
        ('Absent', 'Absent'),
        ('Rest Day', 'Rest Day'),
    ]

    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.DateTimeField(null=True, blank=True)  # Auto-convert to Manila time
    time_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Absent')
    
    # Historical schedule snapshot
    scheduled_start = models.TimeField()  
    scheduled_end = models.TimeField()
    is_rest_day = models.BooleanField()
    
    # Tracking
    late_minutes = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['employee', 'date']

    def save(self, *args, **kwargs):
        # Always use Manila timezone
        manila_tz = pytz.timezone('Asia/Manila')
        
        # Capture schedule snapshot
        self._capture_schedule(manila_tz)
        
        # Calculate status
        if not self.is_rest_day and self.time_in:
            self._calculate_lateness(manila_tz)
        
        super().save(*args, **kwargs)

    def _capture_schedule(self, tz):
        """Creates an Immutable/Unchangeable record of the employee's schedule for that day
        Example: Employee A has a schedule in monday of 8:00 A.M. to 5:00 P.M.
        This method will copy that schedule for the day so even if that employee's schedule
        changes, there will be historical records of what their schedule for that day of the week is."""
        try:
            schedule = self.employee.employeeschedule
            day_of_week = self.date.strftime('%A').lower()
            self.scheduled_start = getattr(schedule, f"{day_of_week}_start")
            self.scheduled_end = getattr(schedule, f"{day_of_week}_end")
            self.is_rest_day = not (self.scheduled_start and self.scheduled_end)
        except EmployeeSchedule.DoesNotExist:
            self.is_rest_day = True

    def _calculate_lateness(self, tz):
        #convert time_in to Manila Time
        manila_time_in = self.time_in.astimezone(tz)
        
        #build scheduled datetime with midnight shift handling
        base_date = self.date
        scheduled_start_dt = tz.localize(datetime.combine(base_date, self.scheduled_start))
        
        #handle end time next day if needed
        if self.scheduled_end < self.scheduled_start:
            scheduled_end_dt = tz.localize(
                datetime.combine(base_date + timedelta(days=1), self.scheduled_end)
            )
        else:
            scheduled_end_dt = tz.localize(datetime.combine(base_date, self.scheduled_end))

        #compute for lateness
        grace_cutoff = scheduled_start_dt + timedelta(
            minutes=self.employee.grace_period_minutes
        )
        
        if manila_time_in > grace_cutoff:
            self.late_minutes = (manila_time_in - scheduled_start_dt).seconds // 60
            self.status = 'Late'
        else:
            self.status = 'On-Time'
            
