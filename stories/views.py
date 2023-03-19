from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Story, Comment
from .forms import StoryForm, CategoryForm, TagForm, CommentForm

# Create your views here.


@login_required
def create_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        category_form = CategoryForm(request.POST)
        tag_form = TagForm(request.POST)

        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user

            if category_form.is_valid():
                category_name = category_form.cleaned_data['name']
                category = Category.objects.get_or_create(name=category_name)
                story.category = category
            story.save()

            if tag_form.is_valid():
                tag_name = tag_form.cleaned_data['name']
                tag = Tag.objects.get_or_create(name=tag_name)
                story.tags.add(tag)

            return redirect('stories:index')
    else:
        form = StoryForm()
        category_form = CategoryForm()
        tag_form = TagForm()

    context = {'form': form, 'category_form': category_form,
               'tag_form': tag_form}
    return render(request, 'stories/create_story.html', context)


def index(request):
    stories = Story.objects.all()
    return render(request, 'stories/index.html', {'stories': stories})


def home(request):
    stories = Story.objects.all().order_by('-created')[:30]
    context = {
        'stories': stories,
    }
    return render(request, 'stories/home.html', context)


def story_detail(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    return render(request, 'stories/story_detail.html', {'story': story})


@login_required
def add_comment(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.story = story
            comment.user = request.user
            comment.save()
            return redirect('stories:story_detail', story_id=story.id)
    else:
        form = CommentForm()

    context = {
        'story': story,
        'form': form
    }
    return render(request, 'stories/story_detail.html', context)
