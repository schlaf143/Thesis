from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError

# Employee model
class Employee(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
    ]
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    address = models.TextField()
    email_address = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# User model
class User(AbstractBaseUser):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='user')
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['employee']

    def __str__(self):
        return self.username

# Shift model
class Shift(models.Model):
    shift_id = models.AutoField(primary_key=True)
    shift_type = models.CharField(max_length=50)
    est_time_in = models.TimeField()
    est_time_out = models.TimeField()

    def __str__(self):
        return self.shift_type

# Branch model
class Branch(models.Model):
    branch_id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=100)
    branch_address = models.TextField()
    branch_ip_address = models.GenericIPAddressField()

    def __str__(self):
        return self.branch_name
# Day model    
class Day(models.Model):
    day_name = models.CharField(
        max_length=3,
        choices=[
            ('Mon', 'Monday'),
            ('Tue', 'Tuesday'),
            ('Wed', 'Wednesday'),
            ('Thu', 'Thursday'),
            ('Fri', 'Friday'),
            ('Sat', 'Saturday'),
            ('Sun', 'Sunday'),
        ],
        unique=True
    )

    def __str__(self):
        return self.day_name


# Employee Schedule model
class EmployeeSchedule(models.Model):
    employee_schedule_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='schedules')
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='schedules')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='schedules')
    days = models.ManyToManyField(Day, related_name='employee_schedules')

    class Meta:
        constraints = [
            # Prevent overlapping schedules for the same employee on the same branch and day
            models.UniqueConstraint(
                fields=['employee', 'shift', 'branch'],
                name='unique_employee_schedule'
            )
        ]
        indexes = [
            models.Index(fields=['employee', 'branch', 'shift']),
        ]

    def __str__(self):
        day_list = ", ".join([day.day_name for day in self.days.all()])
        return f"{self.employee} - {self.shift.shift_type} at {self.branch.branch_name} on {day_list}"
    
    def clean(self):
            # Ensure no duplicate schedules for the same employee, branch, and day
            overlapping_schedules = EmployeeSchedule.objects.filter(
                employee=self.employee,
                branch=self.branch,
                shift=self.shift,
            ).exclude(pk=self.pk)  # Exclude the current instance during update

            if overlapping_schedules.exists():
                raise ValidationError(
                    f"Employee {self.employee} already has a schedule at {self.branch.branch_name} with shift {self.shift.shift_type}."
                )

    def save(self, *args, **kwargs):
        self.clean()  # Run validations before saving
        super().save(*args, **kwargs)

# Attendance model
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('On Leave', 'On Leave'),
    ]
    TAG_CHOICES = [
        ('Regular', 'Regular'),
        ('Overtime', 'Overtime'),
    ]

    attendance_id = models.AutoField(primary_key=True)
    employee_schedule = models.ForeignKey(EmployeeSchedule, on_delete=models.CASCADE, related_name='attendances')
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, blank=True, null=True)
    current_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_schedule} - {self.current_date}"
