# Generated by Django 4.1.7 on 2023-03-28 00:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0015_vote_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='vote_type',
        ),
    ]