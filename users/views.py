from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import is_valid_path
from stories.models import Story, Comment

from .forms import CustomUserCreationForm
from .models import UserProfile

# Create your views here.


@login_required
def profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    user_stories = Story.objects.filter(user=user).order_by('-created')
    user_comments = Comment.objects.filter(
        user=user).order_by('-created')

    context = {
        'user': user,
        'user_profile': user_profile,
        'user_stories': user_stories,
        'user_comments': user_comments,
    }
    return render(request, 'users/profile.html', context)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create the UserProfile
            profile = UserProfile(user=user)
            profile.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
