from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User, Group
from .models import UsersAccount, Profile

@receiver(post_save, sender=UsersAccount)
def create_profile(sender, instance, created, **kwargs):
	
	if created:
		# group = Group.objects.create(name='admin')
		# instance.groups.add(group)
		Profile.objects.create(user=instance, first_name=instance.full_name)
		print('Profile created!')

#post_save.connect(create_profile, sender=User)

@receiver(post_save, sender=UsersAccount)
def update_profile(sender, instance, created, **kwargs):
	
	if created == False:
		instance.profile.save()
		print('Profile updated!')


#post_save.connect(update_profile, sender=User)