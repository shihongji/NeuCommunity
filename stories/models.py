from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from simplemde.fields import SimpleMDEField

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Story(models.Model):
    title = models.CharField(max_length=255, unique=True)
    url = models.URLField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=int(0))
    favorites = models.ManyToManyField(
        User, related_name='favorites', blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def num_comments(self):
        return self.comments.count()

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(
        Story, related_name='comments', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        'self', on_delete=CASCADE, null=True, blank=True, related_name='replies')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    upvotes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"
