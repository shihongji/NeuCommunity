from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Count, Q
from .models import Story, Comment, Tag, Vote
from .forms import StoryForm, CommentForm

# Create your views here.


def search(request):
    query = request.GET.get('q', '')
    if query:
        stories = Story.objects.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
        count = stories.count()
    else:
        stories = Story.objects.none()
        count = 0

# Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(stories, 50)
    page_obj = paginator.get_page(page_number)

    context = {
        'stories': page_obj,
        'query': query,
        'count': count,
    }
    return render(request, 'stories/search.html', context)


@login_required
def create_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)

        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            # story.tags.set(form.cleaned_data['tags'])
            return redirect('stories:home')
    else:
        form = StoryForm()

    context = {'form': form}
    return render(request, 'stories/create_story.html', context)


# Obselete
def index(request):
    stories = Story.objects.all()
    return render(request, 'stories/index.html', {'stories': stories})


def home(request):
    order_by = request.GET.get('order_by', '-votes')
    category_filter = request.GET.get('category', None)

    if order_by == 'votes':
        order_by = '-votes'
    elif order_by == 'new':
        order_by = '-created'
    elif order_by == '-created':
        order_by = '-created'
    else:
        order_by = '-votes'

    if category_filter:
        stories_list = Story.objects.annotate(
            num_upvotes=Count('vote', filter=Q(vote__vote_type=True))
        ).filter(category__name__iexact=category_filter).order_by(order_by)
    else:
        stories_list = Story.objects.annotate(
            num_upvotes=Count('vote', filter=Q(vote__vote_type=True))
        ).order_by(order_by)

    # Show 20 stories per page
    paginator = Paginator(stories_list, 30)

    page = request.GET.get('page')
    stories = paginator.get_page(page)

    context = {
        'stories': stories,
        'order_by': order_by,
        'category_filter': category_filter,
    }
    return render(request, 'stories/home.html', context)


@login_required
def story_detail(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    is_owner = story.user == request.user
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
        parent_comment__isnull=True
    ).annotate(
        num_upvotes=Count('vote', filter=Q(vote__vote_type=True))
    ).order_by('-num_upvotes', '-created')
    context = {
        'story': story,
        'form': form,
        'root_comments': root_comments,
        'is_owner': is_owner,
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

# Upvote


@login_required
def upvote_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    vote = Vote.objects.filter(user=request.user, story=story).first()
    if not vote:
        vote = Vote(user=request.user, story=story, vote_type=True)
        vote.save()
        story.votes += 1
        story.save()
        messages.success(request, "Upvote added.")
    else:
        messages.error(request, "You have already voted for this story.")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def upvote_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    vote = Vote.objects.filter(user=request.user, comment=comment).first()
    if not vote:
        vote = Vote(user=request.user, comment=comment, vote_type=True)
        vote.save()
        comment.votes += 1
        comment.save()
        messages.success(request, "Upvote added.")
    else:
        messages.error(request, "You have already voted for this comment.")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def is_story_owner(function):
    def wrap(request, *args, **kwargs):
        story_id = kwargs['story_id']
        story = get_object_or_404(Story, id=story_id)

        if not request.user.is_authenticated:
            messages.error(request, "You need to login first.")
            return redirect(reverse('login'))

        if not story.user == request.user:
            messages.error(
                request, "You do not have permission to perform this action.")
            return redirect(reverse('stories:story_detail', args=[story_id]))

        return function(request, *args, **kwargs)

    return wrap


@is_story_owner
def edit_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    if request.method == 'POST':
        form = StoryForm(request.POST, instance=story)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post has been updated.')
            return redirect(reverse('stories:story_detail', args=[story_id]))
    else:
        form = StoryForm(instance=story)

    context = {
        'form': form,
    }
    return render(request, 'stories/create_story.html', context)
    # Autocomlete searth for tags, Add an endpoint to fetch tags.

    # @login_required
    # def search_tags(request):
    #     query = request.GET.get('query', '').strip()
    #     if query:
    #         tags = Tag.objects.filter(name__icontains=query).values('name')
    #         return JsonResponse(list(tags), safe=False)
    #     else:
    #         return JsonResponse([], safe=False)
