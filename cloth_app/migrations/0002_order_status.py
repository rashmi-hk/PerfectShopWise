# Generated by Django 4.2.2 on 2023-08-04 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloth_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('PROCESSING', 'Processing'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')], default='PENDING', max_length=20),
        ),
    ]
