# Generated by Django 5.0.7 on 2024-09-24 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_booking_hall_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='hall_id',
            new_name='hall',
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='user_id',
            new_name='user',
        ),
    ]
