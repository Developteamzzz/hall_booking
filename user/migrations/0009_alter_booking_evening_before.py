# Generated by Django 5.0.7 on 2024-09-25 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_booking_evening_before'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='evening_before',
            field=models.CharField(default='no', max_length=3, null=True),
        ),
    ]
