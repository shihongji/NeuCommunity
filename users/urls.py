from . import views
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('profile/<str:username>/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('edit_profile/', views.update_profile, name='edit'),
]
