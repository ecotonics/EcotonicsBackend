# Generated by Django 5.2.1 on 2025-05-29 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Workforce', '0007_alter_staff_status'),
        ('Works', '0015_alter_work_staffs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oncall',
            name='staffs',
            field=models.ManyToManyField(blank=True, to='Workforce.staff'),
        ),
    ]
