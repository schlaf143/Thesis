# Generated by Django 5.1.7 on 2025-05-19 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_leaverequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaverequest',
            name='department_approval',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED')], default='PENDING', max_length=10),
        ),
        migrations.AlterField(
            model_name='leaverequest',
            name='hr_approval',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED')], default='PENDING', max_length=10),
        ),
        migrations.AlterField(
            model_name='leaverequest',
            name='president_approval',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED')], default='PENDING', max_length=10),
        ),
        migrations.AlterField(
            model_name='leaverequest',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED')], default='PENDING', max_length=10),
        ),
    ]
