# Generated by Django 4.2.5 on 2023-09-13 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_doctor_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='pictures/'),
        ),
    ]
