from django.urls import path
from . import views

app_name = 'stories'

urlpatterns = [
    path('', views.home, name='home'),
    path('submit', views.create_story, name='create_story'),
    path('story/<int:story_id>/', views.story_detail, name='story_detail'),
    path('story/<int:story_id>/add_comment/',
         views.add_comment, name='add_comment'),
]
