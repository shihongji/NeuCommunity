from . import views
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
]
