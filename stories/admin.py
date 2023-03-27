from django.contrib import admin
from .models import Story, Category, Comment, Vote
# Register your models here.

admin.site.register(Story)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Vote)
