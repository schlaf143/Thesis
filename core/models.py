from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError


class Employee(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    ROLE_CHOICES = [
        ('Employee', 'Employee'),
        ('HR', 'Human Resources'),
        ('Admin', 'Administrator'),
    ]

    employee_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    company_id = models.CharField(max_length=20, blank=False)  # Changed to CharField
    first_name = models.CharField(max_length=100, blank=False)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=False)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=False)
    role = models.CharField(max_length=8, choices=ROLE_CHOICES, default='Employee', blank=False)
    department = models.CharField(max_length=100, blank=False)
    contact_number = models.CharField(max_length=15, blank=False)
    date_employed = models.DateField()
    leave_credits = models.IntegerField(default=0, blank=False)

    class Meta:
        ordering = ['last_name', 'first_name']  # Default ordering
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        db_table = 'employee_table'  # Custom database table name
        constraints = [
            models.UniqueConstraint(
                fields=['company_id', 'employee_id'], name='unique_company_employee'
            ),
            models.CheckConstraint(
                check=models.Q(leave_credits__gte=0),
                name='positive_leave_credits',
            ),
        ]

    def clean(self):
        if Employee.objects.filter(company_id=self.company_id, employee_id=self.employee_id).exists():
            raise ValidationError("This combination of Company ID and Employee ID already exists.")
        if self.leave_credits < 0:
            raise ValidationError("Leave credits cannot be negative.")
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"