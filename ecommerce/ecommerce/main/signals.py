from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import CustomUser, Profile
from django.contrib.auth.models import Group


@receiver(post_save, sender = CustomUser, dispatch_uid = 'signal_1')
def default_group(sender, instance, **kwargs):
    group, is_created = Group.objects.get_or_create(name='Common Users')
    instance.groups.add(group)

@receiver(post_save, sender = Profile, dispatch_uid = 'signal_1')
def default_group(sender, instance, **kwargs):
    group, is_created = Group.objects.get_or_create(name='Common Users')
    instance.groups.add(group)