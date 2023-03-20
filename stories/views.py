from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
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

            return redirect('stories:home')
    else:
        form = StoryForm()
        category_form = CategoryForm()
        tag_form = TagForm()

    context = {'form': form, 'category_form': category_form,
               'tag_form': tag_form}
    return render(request, 'stories/create_story.html', context)


# Obselete
def index(request):
    stories = Story.objects.all()
    return render(request, 'stories/index.html', {'stories': stories})


def home(request):
    order_by = request.GET.get('order_by', 'votes')
    category_filter = request.GET.get('category', None)

    if order_by == 'votes':
        order_by = '-upvotes'
    elif order_by == 'new':
        order_by = '-created'
    else:
        order_by = '-upvotes'

    if category_filter:
        stories_list = Story.objects.filter(
            category__name__iexact=category_filter).order_by(order_by)
    else:
        stories_list = Story.objects.all().order_by(order_by)

    # Show 20 stories per page
    paginator = Paginator(stories_list, 20)

    page = request.GET.get('page')
    stories = paginator.get_page(page)

    context = {
        'stories': stories,
    }
    return render(request, 'stories/home.html', context)


def story_detail(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.story = story
            comment.user = request.user

            parent_id = request.POST.get('parent_comment')
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                comment.parent_id = parent_id

            comment.save()
            return redirect('stories:story_detail', story_id=story_id)
    else:
        form = CommentForm()

    root_comments = story.comments.filter(
        parent_comment__isnull=True).order_by('-upvotes')
    context = {
        'story': story,
        'form': form,
        'root_comments': root_comments,
    }
    return render(request, 'stories/story_detail.html', context)


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

# Upvote for comment


def upvote_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.upvotes += 1
    comment.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))
