# Generated by Django 5.0.6 on 2024-07-04 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_alter_mailingsettings_periodicity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailingreport',
            name='first_attempt_time',
        ),
    ]