# Generated by Django 4.2.20 on 2025-04-29 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0007_remove_customer_status_customer_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='auto_id',
            field=models.PositiveIntegerField(blank=True, db_index=True, editable=False, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='followup',
            name='auto_id',
            field=models.PositiveIntegerField(blank=True, db_index=True, editable=False, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='lead',
            name='auto_id',
            field=models.PositiveIntegerField(blank=True, db_index=True, editable=False, null=True, unique=True),
        ),
    ]
