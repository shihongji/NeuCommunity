from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
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
            messages.success(request, "You have successfully logged in.")
            next_url = request.GET.get('next', None)
            if next_url:
                return redirect(next_url)
            else:
                return redirect(reverse('stories:home'))

        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'users/login.html')

    else:
        return render(request, 'users/login.html')


def custom_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('stories:home'))


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
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
        print("I'm POSTing")
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print("I'm valid, then save")
            user = form.save()
            print("I'm saving")
            # UserProfile will be created automatically by the post_save signal, so I comment below.
            # Create the UserProfile
            # profile = UserProfile(user=user)
            # profile.save()
            login(request, user)
            return redirect('stories:home')
        else:
            messages.error(
                request, 'There was an error with your registration. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
        print("I'm creating new")
    return render(request, 'registration/registersty.html', {'form': form})
