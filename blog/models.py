from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    index = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=False)
    cover = models.ForeignKey('blog.Image', on_delete=models.CASCADE, related_name='cover', null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    survey_is_present = models.BooleanField(default=False)
    question = models.CharField(max_length=200, blank=True, null=True)
    type_of_vote = models.BooleanField(default=True)
    url = models.CharField(max_length=200, default=True)
    video = models.BooleanField(default=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
class Ad_Block(models.Model):
    link = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)
    image = models.ForeignKey('blog.Image', on_delete=models.CASCADE, related_name='ad_block', null=True)
    active = models.BooleanField(default=True)

class Comment(models.Model):
    author = models.CharField(max_length=200, null=True)
    text = models.TextField(null=True)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    created_date = models.DateTimeField(default=timezone.now)
    photo_of_user = models.ImageField(upload_to="blog/static/media/", blank=True)
    by_administration = models.BooleanField(default=False)
    by_authenticated = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="blog/static/media/", blank=True)
    darktheme = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    is_premium = models.BooleanField(default=False)

class Like(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='likes')
    date = models.DateTimeField(blank=True, null=True)

class Survey(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='survey', null=True)
    variant = models.CharField(max_length=200)
    count = models.PositiveIntegerField(default=0)

class View(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='view')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(blank=True, null=True)

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    variant = models.ForeignKey('blog.Survey', on_delete=models.CASCADE, related_name='vote')

class NewsPapper(models.Model):
    title = models.CharField(max_length=200)
    pdf = models.FileField(upload_to="blog/static/media/",null=True, blank=True)
    date = models.DateTimeField(blank=True, null=True)

class Ad(models.Model):
    contact = models.CharField(max_length=200)
    text = models.TextField()
    remove_date = models.PositiveIntegerField(default=0)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

class Image(models.Model):
    image = models.ImageField(upload_to="blog/static/media/",null=True, blank=True)
    upload_date = models.DateTimeField(default=timezone.now)

class Tag(models.Model):
    tag = models.CharField(max_length=200, null=True)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='tags', null=True)

class Report(models.Model):
    comment = models.ForeignKey('blog.Comment', on_delete=models.CASCADE, related_name='reports')