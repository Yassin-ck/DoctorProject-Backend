# Generated by Django 4.2.5 on 2023-09-15 16:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_doctor_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mufees', to=settings.AUTH_USER_MODEL),
        ),
    ]
