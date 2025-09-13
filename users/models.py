# users/models.py
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_trainer = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Profile"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('trainee', 'Trainee'),
        ('trainer', 'Trainer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='trainee')

    def __str__(self):
        return self.username
