from typing import Union, Optional
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from stories.models import Story, Comment
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm, UserProfileForm
from .models import UserProfile


def custom_login(request: HttpRequest) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    Custom user login view.
    Handles authentication and redirects user based on login status.
    """
    if request.method == "POST":
        username: str = request.POST.get["username", ""]
        password: str = request.POST.get["password", ""]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            next_url: Optional[str] = request.GET.get("next", reverse("stories:home"))
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "users/login.html")


def custom_logout(request: HttpRequest) -> HttpResponseRedirect:
    """
    Custom user logout view that logs out the user and redirects to the home page.
    """
    logout(request)
    return HttpResponseRedirect(reverse("stories:home"))


@login_required
def profile(request: HttpRequest, username: str) -> HttpResponse:
    """
    Display a user's profile page.
    Shows the user's profile, stories, and comments.
    """
    user: User = get_object_or_404(User, username=username)
    user_profile: UserProfile = user.userprofile
    user_stories = Story.objects.filter(user=user).order_by("-created")
    user_comments = Comment.objects.filter(user=user).order_by("-created")
    is_owner: bool = user == request.user

    context = {
        "user": user,
        "user_profile": user_profile,
        "user_stories": user_stories,
        "user_comments": user_comments,
        "is_owner": is_owner,
    }
    return render(request, "users/profile.html", context)


def register(request: HttpRequest) -> HttpResponse:
    """
    User registration view.
    Registers a new user and logs them in.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("stories:home")
        else:
            messages.error(
                request,
                "There was an error with your registration. Please correct the errors below.",
            )
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def update_profile(request: HttpRequest) -> HttpResponse:
    """
    Allows logged-in users to update their profile information.
    """
    user_profile: UserProfile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect(reverse("users:profile", args=[request.user]))
    else:
        form = UserProfileForm(instance=user_profile)

    context = {"form": form}
    return render(request, "users/update_profile.html", context)
