# Generated by Django 5.1.3 on 2025-01-03 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_employeeschedule_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.CharField(choices=[('Employee', 'Employee'), ('Department Head', 'Department Head'), ('Admin', 'Administrator')], default='Employee', max_length=20),
        ),
        migrations.AlterField(
            model_name='employee',
            name='sex',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Prefer not to Say')], max_length=20),
        ),
    ]