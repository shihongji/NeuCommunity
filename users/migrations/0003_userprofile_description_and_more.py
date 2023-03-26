# Generated by Django 4.1.7 on 2023-03-26 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile_blog_site_userprofile_github_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='instagram_address',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='Instagram'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='twitter_address',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='Twitter'),
        ),
    ]
