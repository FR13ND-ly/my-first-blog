from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment, Profile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title',)

class CommentForm(forms.ModelForm):
    class Meta:
    	model = Comment
    	fields = ()
