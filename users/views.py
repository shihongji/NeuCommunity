from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.forms import UserCreationForm
from django.urls import is_valid_path, reverse
from django.http import HttpResponse, HttpResponseRedirect
from stories.models import Story, Comment
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm
from .models import UserProfile

# Create your views here.


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('stories:home'))
        else:
            return HttpResponse("Invalid username or password.")

    return render(request, 'users/login.html')


def custom_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('stories:home'))


@login_required
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile = user.userprofile
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
