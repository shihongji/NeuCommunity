from django.urls import path
from . import views

app_name = 'stories'

urlpatterns = [
    path('', views.index, name='index'),
    path('submit', views.create_story, name='create_story'),
]
