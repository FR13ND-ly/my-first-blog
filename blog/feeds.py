from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post
from django.utils import timezone

class LatestPostsFeed(Feed):
    title = 'My blog'
    link = '/blog/'
    description = 'New posts of my blog.'

    def items(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')[0:5]

    def item_title(self, item):
        return Post.title

    def item_description(self, item):
        return truncatewords(Post.text, 30)