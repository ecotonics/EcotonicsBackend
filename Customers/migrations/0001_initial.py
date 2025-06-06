# Generated by Django 5.1.4 on 2025-01-11 10:34

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('auto_id', models.PositiveIntegerField(db_index=True, editable=False, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_updated', models.DateTimeField(blank=True, editable=False, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('individual', 'individual'), ('enterprise', 'enterprise')], max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=50)),
                ('mobile', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
                'ordering': ('-date_added',),
            },
        ),
        migrations.CreateModel(
            name='Followup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('auto_id', models.PositiveIntegerField(db_index=True, editable=False, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_updated', models.DateTimeField(blank=True, editable=False, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date', models.DateField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('details', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Followup',
                'verbose_name_plural': 'Followups',
                'ordering': ('-date_added',),
            },
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('auto_id', models.PositiveIntegerField(db_index=True, editable=False, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('date_updated', models.DateTimeField(blank=True, editable=False, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('CONVERTED', 'CONVERTED'), ('FAILED', 'FAILED')], default='PENDING', max_length=50)),
                ('is_update_allowed', models.BooleanField(default=True)),
                ('type', models.CharField(choices=[('individual', 'individual'), ('enterprise', 'enterprise')], max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=50)),
                ('mobile', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('info', models.TextField(blank=True, null=True)),
                ('primary_requirements', models.TextField(blank=True, null=True)),
                ('scope_of_work', models.TextField(blank=True, null=True)),
                ('site_condetion', models.TextField(blank=True, null=True)),
                ('additional_requirements', models.TextField(blank=True, null=True)),
                ('customer_preferences', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Lead',
                'verbose_name_plural': 'Leads',
                'ordering': ('-date_added',),
            },
        ),
    ]
