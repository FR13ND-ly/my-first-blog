from django.contrib import admin
from .models import Post, Comment, Like, Ad

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Ad)
# Register your models here.
