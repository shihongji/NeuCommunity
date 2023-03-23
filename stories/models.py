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
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='stories')
    created = models.DateTimeField(auto_now_add=True)
    favorites = models.ManyToManyField(
        User, related_name='favorites', blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def num_comments(self):
        return self.comments.count()

    def __str__(self):
        return self.title

    def votes(self):
        upvotes = self.vote_set.filter(vote_type=True).count()
        downvotes = self.vote_set.filter(vote_type=False).count()
        return upvotes - downvotes


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    story = models.ForeignKey(
        Story, related_name='comments', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        'self', on_delete=CASCADE, null=True, blank=True, related_name='replies')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"

    def votes(self):
        upvotes = self.vote_set.filter(vote_type=True).count()
        downvotes = self.vote_set.filter(vote_type=False).count()
        return upvotes - downvotes


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    story = models.ForeignKey(Story, on_delete=CASCADE, null=True, blank=True)
    comment = models.ForeignKey(
        Comment, on_delete=CASCADE, null=True, blank=True)
    # True for upvote, False for downvote
    vote_type = models.BooleanField(default=True)
