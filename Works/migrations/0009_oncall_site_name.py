# Generated by Django 4.2.20 on 2025-04-29 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Works', '0008_alter_attendance_auto_id_alter_oncall_auto_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='oncall',
            name='site_name',
            field=models.CharField(default='a new site', max_length=100),
            preserve_default=False,
        ),
    ]
