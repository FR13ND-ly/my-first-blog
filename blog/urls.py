from django.urls import path ,include
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as authViews

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('articol/<str:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('articol/<str:pk>/edit/', views.post_edit, name='post_edit'),
    path('articol/<str:pk>/remove/', views.post_remove, name='post_remove'),
 	path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
	path('comment/<int:pk>/report/', views.report_comment, name='report_comment'),
	path('comment/<int:pk>/approve/', views.approve_comment, name='approve_comment'),
 	path('pagina/<str:lk>', views.post_list_next, name='choose_page'),
 	path('login/', views.user_login, name='login'),
 	path('register/', views.register, name='register'),
 	path('logout/', views.user_logout, name='logout' ),
 	path('articol/<str:pk>/like', views.add_like, name='add_like'),
 	path('articol/<str:pk>/vote', views.vote, name="vote"),
 	path('setusertheme/<int:theme>', views.setusertheme, name='setusertheme'),
 	path('ads', views.ads_list, name='ads'),
	path('ads/new/', views.ad_new, name='new_ad'),
	path('ads/<int:pk>/', views.ad_edit, name="ad_edit"),
	path('ads/<int:pk>/remove', views.ad_delete, name="ad_delete"),
	path('search', views.search, name="search"),
	path('search_by_tag/<str:tag>/', views.search_by_teg, name="search_by_tag"),
	path('statistics', views.statistics, name="statistics"),
	path('reports', views.report_page, name="reports_page"),
	path('lista_imaginilor', views.image_list, name="image_list"),
	path('activitatea_mea', views.history, name="history"),
	path('side_menu', views.edit_side, name="edit_side_menu"),
	path('ziar_online', views.online_newspapper, name="online_newspapper"),
	path('test', views.test_page, name="test"),
   ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
