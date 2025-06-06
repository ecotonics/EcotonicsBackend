# Generated by Django 5.1.4 on 2025-01-11 10:34

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('auto_id', models.PositiveIntegerField(db_index=True, editable=False, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_updated', models.DateTimeField(blank=True, editable=False, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=50)),
                ('info', models.TextField(blank=True, null=True)),
                ('creator', models.ForeignKey(blank=True, editable=False, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator_%(app_label)s_%(class)s_objects', to=settings.AUTH_USER_MODEL)),
                ('updater', models.ForeignKey(blank=True, editable=False, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updater_%(app_label)s_%(class)s_objects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
                'ordering': ('-date_added',),
            },
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('auto_id', models.PositiveIntegerField(db_index=True, editable=False, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_updated', models.DateTimeField(blank=True, editable=False, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=50)),
                ('info', models.TextField(blank=True, null=True)),
                ('creator', models.ForeignKey(blank=True, editable=False, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator_%(app_label)s_%(class)s_objects', to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Workforce.department')),
                ('updater', models.ForeignKey(blank=True, editable=False, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updater_%(app_label)s_%(class)s_objects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Designation',
                'verbose_name_plural': 'Designations',
                'ordering': ('-date_added',),
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('auto_id', models.PositiveIntegerField(db_index=True, editable=False, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_updated', models.DateTimeField(blank=True, editable=False, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('status', models.IntegerField(default=1)),
                ('location', models.CharField(max_length=50)),
                ('aadhar', models.CharField(max_length=12)),
                ('blood', models.CharField(max_length=3)),
                ('contact_name', models.CharField(max_length=50)),
                ('contact_number', models.CharField(max_length=15)),
                ('relation', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=150)),
                ('creator', models.ForeignKey(blank=True, editable=False, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator_%(app_label)s_%(class)s_objects', to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Workforce.department')),
                ('designation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Workforce.designation')),
                ('updater', models.ForeignKey(blank=True, editable=False, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updater_%(app_label)s_%(class)s_objects', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Staff',
                'verbose_name_plural': 'Staffs',
                'ordering': ('-date_added',),
            },
        ),
    ]
