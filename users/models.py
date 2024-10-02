from typing import Optional
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Model to extend the Django User model with additional profile information.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="userprofile"
    )
    favorite_stories = models.ManyToManyField(
        "stories.Story", related_name="favorited_by", blank=True
    )
    description = models.TextField(blank=True, null=True)
    blog_site = models.URLField(
        max_length=255, blank=True, null=True, verbose_name="Blog"
    )
    github_address = models.URLField(
        max_length=255, blank=True, null=True, verbose_name="GitHub"
    )
    linkedin_address = models.URLField(
        max_length=255, blank=True, null=True, verbose_name="LinkedIn"
    )
    twitter_address = models.URLField(
        max_length=255, blank=True, null=True, verbose_name="Twitter"
    )
    instagram_address = models.URLField(
        max_length=255, blank=True, null=True, verbose_name="Instagram"
    )

    def __str__(self):
        return self.user.username
    
    @property
    def get_full_name(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"
    
    @property
    def get_social_links(self) -> Optional[dict]:
        social_links = {
            "blog": self.blog_site,
            "github": self.github_address,
            "linkedin": self.linkedin_address,
            "twitter": self.twitter_address,
            "instagram": self.instagram_address,
        }
        return {key: value for key, value in social_links.items() if value}

@receiver(post_save, sender=User)
def create_user_profile(sender: type[User], instance: User, created: bool, **kwargs) -> None:
    """
    Signal receiver to create a UserProfile instance when a new User is created.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender: type[User], instance: User, **kwargs) -> None:
    """
    Signal receiver to save a UserProfile instance when a User is saved.
    """
    instance.userprofile.save()
