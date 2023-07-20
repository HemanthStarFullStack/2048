# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from django.dispatch import receiver
# from django.utils.module_loading import import_module

# model = import_module('models')

# from models import UserProfile
 

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)