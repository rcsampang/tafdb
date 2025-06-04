from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('regular', 'Regular User'),
        ('admin', 'Administrator'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='regular')
    bio = models.TextField(blank=True, null=True)
    # Add other profile fields if needed, e.g., phone_number, avatar

    def __str__(self):
        return f'{self.user.username} ({self.get_user_type_display()})'

# Signal to create or update UserProfile whenever a User instance is saved.
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # Ensure profile exists, create if not (e.g. for existing users)
        UserProfile.objects.get_or_create(user=instance)
        # instance.profile.save() # If you have fields on profile that need updating based on User model changes
