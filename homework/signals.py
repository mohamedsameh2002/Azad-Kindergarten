from django.dispatch import receiver
from django.db.models.signals import post_save,pre_delete
from .models import Homework
import os




@receiver(pre_delete, sender=Homework)
def delete_homework_images(sender, instance, **kwargs):
    if instance.image_1:  
        if os.path.isfile(instance.image_1.path):
            os.remove(instance.image_1.path)
    if instance.image_2:  
        if os.path.isfile(instance.image_2.path):
            os.remove(instance.image_2.path)
    if instance.image_3:  
        if os.path.isfile(instance.image_3.path):
            os.remove(instance.image_3.path)

@receiver(post_save, sender=Homework)
def delete_old_homeworks(sender, **kwargs):
    homeworks = Homework.objects.all()
    if homeworks.count() > 1200:
        old_homeworks = homeworks.order_by('date')[:600]  
        for homework in old_homeworks:
            homework.delete()
