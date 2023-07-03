import random
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A2L.settings')
django.setup()
from django.core.wsgi import get_wsgi_application
from faker import Faker
from django.contrib.auth.models import User
from stories.models import Story, Category, Comment, Vote
from taggit.managers import TaggableManager


application = get_wsgi_application()


fake = Faker()

# You can customize the categories and tags as needed
categories = ['Ask', 'Jobs', 'News', 'Learn', 'Misllaneous', 'Trading', 'Housing', 'Dining', 'Transportation']
tags = ['Python', 'React', 'JavaScript', 'ML', 'AI', 'Silicon Valley', 'Seattle', 'Boston',
        'San Francisco', 'INFO5100', 'ENCP6000', 'INFO6105', 'Hackathon', 'Algorithm', 'Java']

# Creating categories
for category_name in categories:
    Category.objects.get_or_create(name=category_name)

# Creating tags
# for tag_name in tags:
#     Tag.objects.get_or_create(name=tag_name)

# Generating 200 random stories
for _ in range(200):
    random_user = random.choice(User.objects.all())
    random_category = random.choice(Category.objects.all())
    # random_tags = random.sample(
    #     list(Tag.objects.all()), k=random.randint(1, len(tags)))

    has_url = random.choice([True, False])
    story = Story.objects.create(
        title=fake.sentence(),
        user=random_user,
        category=random_category,
        url=fake.uri() if has_url else None,
        text=fake.text() if not has_url else None,
    )

    story.tags_new.set(random.sample(tags, random.randint(1, len(tags)-5)))
    story.save()

    # Generating random comments for the story
    for _ in range(random.randint(0, 10)):
        comment_user = random.choice(User.objects.all())
        comment = Comment.objects.create(
            user=comment_user,
            story=story,
            text=fake.sentence(),
        )

        # Generating random votes for the comment
        for _ in range(random.randint(0, 5)):
            vote_user = random.choice(User.objects.all())
            Vote.objects.create(
                user=vote_user,
                comment=comment,
                # vote_type=random.choice([True, False]),
            )

    # Generating random votes for the story
    for _ in range(random.randint(0, 20)):
        vote_user = random.choice(User.objects.all())
        Vote.objects.create(
            user=vote_user,
            story=story,
            # vote_type=random.choice([True, False]),
        )

print("200 random stories created with comments and votes!")
