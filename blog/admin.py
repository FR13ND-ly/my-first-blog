from django.contrib import admin
from .models import Post, Comment, Like, Ad, Profile

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Ad)
admin.site.register(Profile)
# Register your models here.
