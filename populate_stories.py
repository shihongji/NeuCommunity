import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A2L.settings')
django.setup()
from stories.models import Story, Category, Tag
from django.contrib.auth.models import User
from faker import Faker
from django.core.wsgi import get_wsgi_application
import random


application = get_wsgi_application()


fake = Faker()

# You can custmorize the categories and tags as needed
categories = ['Ask', 'Jobs', 'Trading', 'Housing', 'Dinning', 'Transportation']
tags = ['Python', 'React', 'JavaScript', 'ML', 'AI', 'Silicon Valley', 'Seatle', 'Boston',
        'San Fransico', 'INFO5100', 'ENCP6000', 'INFO6105', 'Hackerthon', 'Algorithm', 'Java']

# Creating categories
for category_name in categories:
    Category.objects.get_or_create(name=category_name)

# Creating tags
for tag_name in tags:
    Tag.objects.get_or_create(name=tag_name)

# Generating 200 random stories
for _ in range(200):
    random_user = random.choice(User.objects.all())
    random_category = random.choice(Category.objects.all())
    random_tags = random.sample(
        list(Tag.objects.all()), k=random.randint(1, len(tags)))

    story = Story.objects.create(
        title=fake.sentence(),
        user=random_user,
        category=random_category,
        url=fake.uri() if random.choice([True, False]) else None,
        text=fake.text() if not Story.url else None,
    )

    story.tags.set(random_tags)
    story.save()

print("200 random stories created!")
