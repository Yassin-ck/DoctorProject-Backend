from django.dispatch import receiver
from .models import User,Doctor
from django.db.models.signals import post_save

@receiver(post_save,sender=User)
def creating_doctor_instance(sender,instance,created,*args,**kwargs):
    if created and instance.is_doctor:
        Doctor.objects.create(user=instance)