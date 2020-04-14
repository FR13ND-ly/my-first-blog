from django.urls import path ,include
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as authViews

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
 	path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
 	path('page/<int:lk>', views.post_list_next, name='choose_page'),
 	path('login/', views.user_login, name='login'),
 	path('register/', views.register, name='register'),
 	path('logout/', views.user_logout, name='logout' ),
 	path('social-auth/', include('social_django.urls', namespace='social')),
 	path('post/<int:pk>/like', views.add_like, name='add_like'),
 	path('post/<int:pk>/vote', views.vote, name="vote"),
 	path('setusertheme/<int:theme>', views.setusertheme, name='setusertheme'),
 	path('ads', views.ads_list, name='ads'),
	path('ads/new/', views.ad_new, name='new_ad'),
	path('ads/<int:pk>/', views.ad_edit, name="ad_edit"),
	path('ads/<int:pk>/remove', views.ad_delete, name="ad_delete"),
   ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
