# Generated by Django 4.2.5 on 2023-09-14 01:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_doctor_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='image',
        ),
    ]
