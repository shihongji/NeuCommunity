from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_stories = models.ManyToManyField(
        'stories.Story', related_name='favorited_by', blank=True)
    blog_site = models.URLField(
        max_length=255, blank=True, null=True, verbose_name="Blog")
    github_address = models.URLField(
        max_length=255, blank=True, null=True, verbose_name="GitHub")
    linkedin_address = models.URLField(
        max_length=255, blank=True, null=True, verbose_name="LinkedIn")

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
