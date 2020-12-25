import os, random, re
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from datetime import timedelta
from .models import Post, Comment, Profile, Like, Survey, Vote, Ad, Image, Tag, View, Report, Ad_Block, NewsPapper
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from dateutil.relativedelta import relativedelta
import xml.etree.ElementTree as ET
import datetime

def set_dict_for_render(rdict, request):
    if request.user.is_active:
        profile = Profile.objects.get_or_create(user = request.user)
        rdict.update({'profile' : profile})
    if request.user.is_staff:
        rdict.update({'reports' : Report.objects.all()})
    if re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE).match(request.META['HTTP_USER_AGENT']):
        rdict.update({"mobile" : True})
    elif rdict.get('ad_and_side_menu'):
        add_ad_and_side_menu(rdict)
        rdict.update({"mobile" : False})
    return rdict

def check_dark_theme(request):
    if request.user.is_active:
        profile = Profile.objects.get_or_create(user = request.user)[0]
        if profile.darktheme:
            return 'darktheme_'
    return ''

def mobile(request):
    if re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE).match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False

def add_ad_and_side_menu(rdict):
    def get_content(tag):
        if second_ad.active:
            if (tag == 'social' and second_ad_position != 1) or (tag == 'politic' and second_ad_position != 2) or (tag == 'economic' and second_ad_position != 3):
                return Post.objects.select_related('author', 'cover').prefetch_related('view').filter(tags__tag = tag).order_by('published_date').reverse()[:2]
            else:
                return Post.objects.select_related('author', 'cover').prefetch_related('view').filter(tags__tag = tag).order_by('published_date').reverse()[:1]
        else:
            return Post.objects.select_related('cover', 'author').prefetch_related('view').filter(tags__tag = tag).order_by('published_date').reverse()[:2]
    first_ad = Ad_Block.objects.select_related('image').get_or_create(pk = 1)[0]
    second_ad = Ad_Block.objects.select_related('image').get_or_create(pk = 2)[0]
    if second_ad.active:
        second_ad_position = random.randrange(1, 4)
    else:
        second_ad_position = False
    top_posts_dict = {}
    top_posts_points = []
    def check_exist(points):
        if points in top_posts_dict:
            points += 1
            check_exist(points)
        else:
            top_posts_dict[points] = i
            top_posts_points.append(points)
    for i in Post.objects.filter(status = False).select_related('cover', 'author').prefetch_related('view', 'likes').order_by('published_date').reverse()[:15]:
        points = i.view.count()
        points += i.likes.count() * 5
        check_exist(points)
    top_posts_points.sort()
    top_posts_points.reverse()
    tposts = []
    if first_ad.active:
        for tpoints in top_posts_points[ : 2]:
            tposts.append(top_posts_dict[tpoints])
    else:
        for tpoints in top_posts_points[ : 3]:
            tposts.append(top_posts_dict[tpoints])
    extra_posts = Post.objects.select_related('cover').filter(status = False, video = True).order_by('published_date').reverse()[:3]
    rdict.update({"second_ad_fposition" : second_ad_position == 1, "second_ad_sposition" : second_ad_position == 2, "second_ad_tposition" : second_ad_position == 3})    
    rdict.update({"social" : get_content('social')})
    rdict.update({"politic" : get_content('politic')})
    rdict.update({"economic" : get_content('economic')})
    rdict.update({'week_img' : Ad_Block.objects.select_related('image').get_or_create(pk = 0)[0]})
    rdict.update({"first_ad" : first_ad})
    rdict.update({"second_ad" : second_ad})
    rdict.update({"third_ad" : Ad_Block.objects.select_related('image').get_or_create(pk = 3)[0]})
    rdict.update({"e_posts": extra_posts})
    rdict.update({"tposts" : tposts})
    return rdict

def post_list(request):
    if request.user.is_staff:
        relative_number_of_pages = (Post.objects.all().count() - 1) // 5
        posts = Post.objects.all().select_related('author', 'cover').prefetch_related('likes', 'view').order_by('published_date').reverse()[0 : 5]
    else:
        relative_number_of_pages = (Post.objects.filter(status = False).count() - 1) // 5
        posts = Post.objects.filter(status = False).order_by('published_date').select_related('author', 'cover').prefetch_related('likes', 'view').reverse()[0 : 5]
    number_of_pages = []
    index = 0
    for post in posts:
        post.index = index
        index += 1
    for i in range(8):
        if 1 + i < relative_number_of_pages + 2:
            number_of_pages.append(1 + i)
    rendertemplate = {'posts' : posts, 'number_of_pages' : number_of_pages, "current_page" : 1, 'ad_and_side_menu' : True}
    return render(request, 'blog/' + check_dark_theme(request) + 'post_list.html', set_dict_for_render(rendertemplate, request))

def post_list_next(request, lk):
    lk = int(lk)
    if lk == 1:
        return redirect('post_list')
    if request.user.is_staff:
        relative_number_of_pages = (len(Post.objects.all()) - 1) // 5
        posts = Post.objects.all().order_by('published_date').select_related('author', 'cover').prefetch_related('likes', 'view').reverse()
    else:
        relative_number_of_pages = (len(Post.objects.filter(status = False)) - 1) // 5
        posts = Post.objects.filter(status = False).order_by('published_date').select_related('author', 'cover').prefetch_related('likes', 'view').reverse()
    print(relative_number_of_pages)
    if (len(posts) - lk * 5) < 0:
        posts = posts[(lk - 1)* 5 : ]
    else:
        posts = posts[(lk - 1) * 5 : lk * 5]
    number_of_pages = []
    for i in range(4):
        if lk - (4 - i) > 0:
            number_of_pages.append(lk - (4 - i))
    for i in range(4):
        if lk + i < relative_number_of_pages + 2:
            number_of_pages.append(lk + i)
    index = 0
    for post in posts:
        post.index = index
        index += 1
    rendertemplate = {'posts' : posts, 'number_of_pages' : number_of_pages, "current_page" : lk, 'ad_and_side_menu' : True}
    return render(request, 'blog/' + check_dark_theme(request) + 'post_list.html', set_dict_for_render(rendertemplate, request))

def post_detail(request, pk):
    page_post = get_object_or_404(Post, url = pk)
    if request.user.is_active:
        new_view = View.objects.create(post = page_post, user = request.user, date = timezone.now())
        liked = bool(Like.objects.filter(author = request.user, post = page_post))
    else:
        new_view = View.objects.create(post = page_post, date = timezone.now())
        liked = False
    new_view.save()
    survey = Survey.objects.filter(post = page_post)
    uservoted = False
    for variant in survey:
        for i in Vote.objects.filter(variant = variant).select_related('user'):
            if i.user == request.user:
                uservoted = True
    if request.method == "POST" and request.POST.get("add_comment"):
        comment = Comment.objects.create(post = page_post, created_date = timezone.now(), text = request.POST.get('text_of_comment'))
        if request.user.is_active:
            comment.author = request.user.username
            comment.by_authenticated = True
            if request.user.is_staff:
                comment.by_administration = True
        else:
            comment.author = request.POST.get('author_of_comment')
        comment.save()
        print('new comment')
        return redirect('post_detail', pk = page_post.url)
    rendertemplate = {'post' : page_post, 'user' : request.user, 'survey' : survey, 'uservoted' : uservoted, "liked" : liked, 'ad_and_side_menu' : True}
    return render(request, 'blog/' + check_dark_theme(request) + 'post_detail.html', set_dict_for_render(rendertemplate, request))


def comment_remove(request, pk):
    if not request.user.is_staff:
        return redirect('post_list')
    Comment.objects.get(pk = pk).delete()
    print('comment removed')
    return redirect('post_detail', pk=comment.post.url)

def post_new(request):
    if not request.user.is_staff:
        return redirect('post_list')
    if request.method == "POST" and request.POST.get("save_post"):
        post = Post.objects.create(author = request.user, title = request.POST.get("title"), text = request.POST.get("posttext"), published_date = timezone.now())
        post.cover = Image.objects.get(image = request.POST.get("cover_name").replace(" ", "_"))
        tags = request.POST.get('tags_container').split('close')
        for i in tags:
            if i != '':
                if request.POST.get('video') != "on" and i.lower() != "video":
                    new_tag = Tag.objects.create(tag = i, post = post)
                    new_tag.save()
        if request.POST.get('video') == "on":
            post.video = True
            new_tag = Tag.objects.create(tag = 'Video', post = post)
            for i in tags:
                if 'video' == i.lower():
                    for a in post.tags.all():
                        if a.tag.lower() == 'video':
                            if Tag.objects.get_or_create(tag = "Video", post = post)[1]:
                                new_tag.delete()
        else:
            post.video = False
        if request.POST.get('survey_is_present') == "on":
            post.question = request.POST.get('survey_question')
            post.survey_is_present = True
            if request.POST.get('type_of_vote') == "on":
                post.type_of_vote = True
            else:
                post.type_of_vote = False
            for i in request.POST.getlist('variant_of_survey'):
                if i != '':
                    survey = Survey.objects.create(post = post, variant = i)
                    survey.save()
        post.url = post.title.replace(' ', '-')
        post.save()
        print('new post')
        return redirect('post_detail', pk=post.url)
    elif request.method == "POST" and request.FILES.get('file'):
        new_image = Image.objects.create(image = request.FILES.get('file'), upload_date = timezone.now())
        new_image.save()
        print('new image uploaded')
    rendertemplate = {"post_new" : True,"image_list" : Image.objects.all().order_by("upload_date").reverse()}
    return render(request, 'blog/' + check_dark_theme(request) + 'post_edit.html', set_dict_for_render(rendertemplate, request))

def post_edit(request, pk):
    if not request.user.is_staff:
        return redirect('post_list')
    post = Post.objects.get(url = pk)
    surveys = dict()
    a = 0
    for i in Survey.objects.filter(post = post):
        surveys.update({i.variant : a})
        a += 1
    if request.method == "POST" and request.POST.get("save_post"):
        post.title = request.POST.get("title")
        for i in Image.objects.all():
            if (request.POST.get("cover_name") == i.image):
                post.cover = i
        post.text = request.POST.get("posttext")
        for tag in post.tags.all():
            tag.delete()
        tags = request.POST.get('tags_container').split('close')
        for i in tags:
            if i != '':
                new_tag = Tag.objects.create(tag = i, post = post)
                new_tag.save()
        if request.POST.get('status') == "on":
            post.status = True
        else:
            post.status = False
        if request.POST.get('survey_is_present') == "on":
            post.question = request.POST.get('survey_question')
            post.survey_is_present = True
            for i in Survey.objects.filter(post = post):
                i.delete()
            for i in request.POST.getlist('variant_of_survey'):
                if i != '':
                    survey = Survey.objects.create(post = post, variant = i)
                    survey.save()
        else:
            post.survey_is_present = False
        if request.POST.get('video') == "on":
            post.video = True
            new_tag = Tag.objects.create(tag = 'Video', post = post)
            for i in tags:
                if i.lower() == 'video':
                    new_tag.delete()
        else:
            post.video = False
            for i in tags:
                if 'video' == i.lower():
                    for i in post.tags.all():
                        if i.tag.lower() == 'video':
                            i.delete()
        post.url = post.title.replace(' ', '-')
        post.save()
        print('post ' + post.title + ' edited')
        return redirect('post_detail', pk = post.url)
    elif request.method == "POST" and request.FILES.get('file'):
        new_image = Image.objects.create(image = request.FILES.get('file'), upload_date = timezone.now())
        new_image.save()
        print("new image uploaded")
    rendertemplate = {'post' : post, 'surveys':surveys, "image_list" : Image.objects.all().order_by("upload_date").reverse()}
    return render(request, 'blog/' + check_dark_theme(request) + 'post_edit.html', set_dict_for_render(rendertemplate, request))

def post_remove(request, pk):
    if not request.user.is_staff:
        return redirect('post_list')
    post = Post.objects.get(url = pk).delete()
    print('post removed')
    return redirect('post_list')


def user_login(request):
    if request.method == 'POST':
        user = authenticate(username = request.POST.get('logininput'), password = request.POST.get('passwordinput'))
        if user is not None:
            if user.is_active:
                login(request, user)
                if "login" in request.META.get('HTTP_REFERER'):
                    return redirect('post_list')
                else:
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return render(request, 'blog/login.html', {'incorrect_login_or_password' : True})
    return render(request, 'blog/login.html')

def register(request):
    if request.user.is_active:
        return redirect('post_list')
    if request.method == 'POST':
        for i in User.objects.all():
            if i.username == request.POST.get('username'):
                return render(request, 'blog/register.html', {"Error" : "Acest nume de utilizator e ocupat"})
        for i in ['admin', 'administrator', 'est curier', 'estcurier', 'est-curier', 'administrația']:
            if i in request.POST.get('username').lower():
               return render(request, 'blog/register.html', {"Error" : "Numele de utilizator conține un element interzis"})
        if request.POST.get('password') == request.POST.get('repeatedpassword'):
            if len(request.POST.get('password')) > 5:
                user = User.objects.create(username = request.POST.get('username'), email = request.POST.get('email'), date_joined = timezone.now(), password = make_password(request.POST.get('repeatedpassword')))
                user.save()
                profile = Profile.objects.create(user=user)
                profile.save()
                theuser = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
                login(request, theuser)
                print('new user')
                return redirect('post_list')
            else:
                return render(request, 'blog/register.html', {"Error" : "Parola e prea slabă"})
        else:
            return render(request, 'blog/register.html', {"Error" : "Parolele nu coincid"})
    return render(request, 'blog/register.html')

@login_required
def user_logout(request):
    if not request.user.is_active:
        return redirect('post_list')
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def add_like(request, pk):
    post = Post.objects.get(url = pk)
    new_like, created = Like.objects.get_or_create(author = request.user, post = post)
    if created:
        new_like.date = timezone.now()
        new_like.save()
    else:
        like = Like.objects.get(author = request.user, post = post)
        like.delete()
    return redirect('post_detail', pk=post.pk)

@login_required
def vote(request,pk):
    post = Post.objects.get(url = pk)
    if post.type_of_vote:
        survey = Survey.objects.get(post = post, variant = request.POST.get('variant'))
        vote = Vote.objects.create(variant = survey, user = request.user)
        vote.save()
        survey.count = (len(Vote.objects.filter(variant= survey)))
        survey.save()
    else:
        for i in request.POST.getlist('variant'):
            survey = Survey.objects.get(post = post, variant = i)
            vote = Vote.objects.create(variant = survey, user = request.user)
            vote.save()
            survey.count = (len(Vote.objects.filter(variant = survey)))
            survey.save()
    return redirect('post_detail', pk=pk)

@login_required
def setusertheme(request, theme):
    profile = Profile.objects.get(user = request.user)
    profile.darktheme = bool(theme)
    profile.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def ads_list(request):
    ads= Ad.objects.all()
    rendertemplate = {'ads_page' : True, 'ads_list' : True, 'ads' : ads}
    return render(request, 'blog/' + check_dark_theme(request) + 'ads.html',set_dict_for_render(rendertemplate, request))

def ad_new(request):
    if not request.user.is_staff:
        return redirect('post_list')
    if request.method == "POST":
        ad = Ad.objects.create(text = request.POST.get('ad_text'), contact = request.POST.get('contact_data'), published_date = timezone.now(), remove_date = int(request.POST.get('count_of_days')))
        ad.save()
        return redirect('ads')
    rendertemplate = {'ads_page' : True, 'ad_new' : True}
    return render(request, 'blog/' + check_dark_theme(request) + 'ad_edit.html', set_dict_for_render(rendertemplate, request))

def ad_edit(request, pk):
    if not request.user.is_staff:
        return redirect('post_list')
    ad = Ad.objects.get(pk = pk)
    if request.method == "POST":
        ad.text = request.POST.get('ad_text')
        ad.contact = request.POST.get('contact_data')
        ad.remove_date = int(request.POST.get('count_of_days'))
        ad.save()
        return redirect('ads')
    rendertemplate = {'ads_page' : True, 'ad' : ad}
    return render(request, 'blog/' + check_dark_theme(request) + 'ad_edit.html', set_dict_for_render(rendertemplate, request))

def ad_delete(request, pk):
    if not request.user.is_staff:
        return redirect('post_list')
    ad = Ad.objects.get(pk = pk).delete()
    return redirect('ads')

def test_page(request):
    return render(request, 'blog/test.html')

def search(request):
    def prepare(word):
        return word.lower().replace('ț', 't').replace('ș', 's').replace('î', 'i').replace('â', 'a').replace('ă', 'a')

    def prepare_word_list(word_list):
        for i in ["și", "sau", "de", "care", "la", "a", "fi", "eu", "ea", "el", "dar", "tu"]:
            if i in word_list:
                word_list.remove(i)
        return word_list
    words_list = prepare_word_list(request.GET.get('search').split(' '))
    posts = []
    ads = []
    comments = []
    for word in words_list:
        for post in Post.objects.all().order_by("published_date").reverse().select_related('cover', 'author').prefetch_related('view', 'likes'):
            for word_of_title in prepare_word_list(post.title.split(" ")):
                if prepare(word_of_title) == prepare(word) and post not in posts:
                    posts.append(post)
            for word_of_text in prepare_word_list(post.text.split(' ')):
                if prepare(word_of_text) == prepare(word) and post not in posts:
                    posts.append(post)
        for ad in Ad.objects.all().order_by("published_date").reverse():
            for word_of_ad in prepare_word_list(ad.text.split(" ")):
                if prepare(word_of_ad) == prepare(word) and ad not in ads:
                    ads.append(ad)
        for comment in Comment.objects.all().order_by("created_date").reverse().select_related('post'):
                for word_of_comment in prepare_word_list(comment.text.split(" ")):
                    if prepare(word_of_comment) == prepare(word) and comment not in comments:
                        comments.append(comment)
    rendertemplate = {"posts" : posts, "ads" : ads, "comments" : comments, "search_page" : True, 'search_item' : request.GET.get('search')}
    return render(request, 'blog/' + check_dark_theme(request) + 'search_page.html', set_dict_for_render(rendertemplate, request))

def search_by_teg(request, tag):
    posts = Post.objects.select_related('cover', 'author').prefetch_related('view', 'likes').filter(tags__tag = tag).order_by('published_date').reverse()[:2]
    rendertemplate = {"posts" : posts, 'hide_ads_and_comments' : True, 'search_by_teg' : True}
    return render(request, 'blog/' + check_dark_theme(request) + 'search_page.html', set_dict_for_render(rendertemplate, request))

def statistics(request):
    if not request.user.is_staff:
        return redirect('post_list')
    Administrators = int()
    Users = int()
    for user in User.objects.all():
        if user.is_staff:
            Administrators += 1
        elif user.is_active and not user.is_staff:
            Users += 1
    Posts = Post.objects.all().count()
    Views = View.objects.all().count()
    Likes = Like.objects.all().count()
    Comments = Comment.objects.all().count()
    views_by_date = {}
    views_by_month = {}
    views_by_year = {}
    views_by_signed_and_not = {"Autentificat" : int(), "Oaspete" : int()}
    white_or_dark_theme_stat = {"Luminoasă" : int(),"Întunecată" : int()}
    comment_by_signed_and_not = {"Autentificați" : int(), "Oaspeți" : int()}
    for i in range(int(timezone.now().strftime("%d")), - 1, - 1):
        views_by_date.update({i : [View.objects.filter(date__date=timezone.now() - timedelta(days = int(timezone.now().strftime("%d")) - i)).reverse().count(), Like.objects.filter(date__date=timezone.now() - timedelta(days = int(timezone.now().strftime("%d")) - i)).reverse().count(), Comment.objects.filter(created_date__date=timezone.now() - timedelta(days = int(timezone.now().strftime("%d")) - i)).reverse().count()] })
    for i in range(int(timezone.now().strftime("%m")), -1, -1):
        views_by_month.update({(timezone.now() - relativedelta(months = int(timezone.now().strftime("%m"))-i)).strftime("%B") : [View.objects.filter(date__date=timezone.now() - relativedelta(months = int(timezone.now().strftime("%m")) - i)).reverse().count(), Like.objects.filter(date__date=timezone.now() - relativedelta(months = int(timezone.now().strftime("%m")) - i)).reverse().count(), Comment.objects.filter(created_date__date=timezone.now() - relativedelta(months = int(timezone.now().strftime("%m")) - i)).reverse().count()] })
    for i in range(int(timezone.now().strftime("%Y")), int(timezone.now().strftime("%Y"))-4, -1):
        views_by_year.update({i : [View.objects.filter(date__date=timezone.now() - relativedelta(years = int(timezone.now().strftime("%Y")) - i)).reverse().count(), Like.objects.filter(date__date=timezone.now() - relativedelta(years = int(timezone.now().strftime("%Y")) - i)).reverse().count(), Comment.objects.filter(created_date__date=timezone.now() - relativedelta(years = int(timezone.now().strftime("%Y")) - i)).reverse().count()] })
    for i in View.objects.all():
        if i.user != None:
            views_by_signed_and_not["Autentificat"] += 1
        else:
            views_by_signed_and_not["Oaspete"] += 1
    for i in Profile.objects.all():
        if i.darktheme:
            white_or_dark_theme_stat["Întunecată"] += 1
        else:
            white_or_dark_theme_stat["Luminoasă"] += 1
    for i in Comment.objects.all():
        if  i.by_authenticated:
            comment_by_signed_and_not["Autentificați"] += 1
        else:
            comment_by_signed_and_not["Oaspeți"] += 1
    rendertemplate = {"Administrators" : Administrators, "Users" : Users, "Posts" : Posts, "Views" : Views, "Likes" : Likes, "Comments" : Comments, "views_by_date" : views_by_date, "views_by_month" : views_by_month, "views_by_year" : views_by_year, 'views_by_signed_and_not' : views_by_signed_and_not , "white_or_dark_theme_stat" : white_or_dark_theme_stat, "comment_by_signed_and_not" : comment_by_signed_and_not}
    return render(request, 'blog/' + check_dark_theme(request) + 'statistic.html', set_dict_for_render(rendertemplate, request))

def report_comment(request, pk):
    comment = Comment.objects.get(pk = pk)
    report = Report.objects.create(comment = comment)
    report.save()
    return redirect('post_detail', pk = comment.post.url)

def report_page(request):
    if not request.user.is_staff:
        return redirect('post_list')
    reported_comments = [] 
    for i in Report.objects.all().select_related('comment'):
        if i.comment not in reported_comments:
            reported_comments.append(i.comment)
    rendertemplate = {"reported_comments" : reported_comments}
    return render(request, 'blog/' + check_dark_theme(request) + 'raport_page.html', set_dict_for_render(rendertemplate, request))
    
def approve_comment(request, pk):
    if not request.user.is_staff:
        return redirect('post_list')
    for i in Comment.objects.get(pk = pk).reports.all():
        i.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def ad_manage(request):
    if not request.user.is_staff:
        return redirect('post_list')
    if request.method == "POST":
        ad = Sidebar_Ad.objects.get_or_create(pk = 0)[1]
        ad.text = request.POST.get('text', "Salut!")
        ad.link = request.POST.get('link')
        if request.FILES.get('image') != None:
            new_image = Image.objects.create(image=request.FILES.get('image'), upload_date = timezone.now())
            new_image.save()
            ad.image = new_image
        ad.save()
    return render(request, 'blog/' + check_dark_theme(request) + 'ad_manage.html', set_dict_for_render({}, request))

def image_list(request):
    if not request.user.is_staff:
        return redirect('post_list')
    elif request.POST.get('remove_image'):
        image = Image.objects.get(pk = request.POST.get('pk'))
        if os.path.exists(os.getcwd().replace("\\", "/") + "/media/" + str(image.image)):
            os.remove(os.getcwd().replace("\\", "/") + "/media/" + str(image.image))
        image.delete()
    elif request.FILES.get('new_image'):
        image = Image.objects.create(image = request.FILES.get('new_image'), upload_date = timezone.now())
        image.save()
    rendertemplate = {"image_list" : Image.objects.all().order_by("upload_date").reverse()}
    return render(request, 'blog/' + check_dark_theme(request) + 'image_list.html', set_dict_for_render(rendertemplate, request))

def history(request):
    if not request.user.is_authenticated:
        return redirect('post_list')
    views = View.objects.filter(user = request.user).order_by("date").reverse().select_related('post').prefetch_related('post__cover', 'post__author', 'post__view', 'post__likes')
    history = {}
    for i in views:
        if len(history) >= 4:
            break
        if (history.get(i.date.date())):
            history[i.date.date()].append(i)
        else:
            history[i.date.date()] = [i]
    rendertemplate = {"third_ad" :  Ad_Block.objects.get_or_create(pk = 3)[0], "history" : history}
    return render(request, 'blog/' + check_dark_theme(request) + 'history.html', set_dict_for_render(rendertemplate, request))

def edit_side(request):
    if not request.user.is_staff:
        return redirect('post_list')
    if request.POST.get('save_ad'):
        changed_ad = Ad_Block.objects.get_or_create(pk = request.POST.get('save_ad'))[0]
        changed_ad.link = request.POST.get("ad_link", "")
        changed_ad.title = request.POST.get("ad_title", "")
        changed_ad.description = request.POST.get("ad_description", "")
        image, exist = Image.objects.get_or_create(image = request.FILES.get('ad_img', changed_ad.image.image))
        if exist:
            image.upload_date = timezone.now()
        if request.POST.get('active') == "on":
            changed_ad.active = True
        else:
            changed_ad.active = False
        image.save()
        changed_ad.image = image
        changed_ad.save()
    rendertemplate = {'week_img' : Ad_Block.objects.select_related('image').get_or_create(pk = 0)[0], 'first_ad' : Ad_Block.objects.select_related('image').get_or_create(pk = 1)[0], 'second_ad' : Ad_Block.objects.select_related('image').get_or_create(pk = 2)[0], 'third_ad' : Ad_Block.objects.select_related('image').get_or_create(pk = 3)[0]}
    return render(request, 'blog/' + check_dark_theme(request) + 'side_ad.html', set_dict_for_render(rendertemplate, request))

def online_newspapper(request):
    if not request.user.is_authenticated:
        return redirect('post_list')
    if request.POST.get('add_pdf'):
        new_np = NewsPapper.objects.create(title = request.POST.get('nr'), pdf = request.FILES.get('pdf'), date = timezone.now())
        new_np.save()
    if request.POST.get('save_pdf_changes'):
        np = NewsPapper.objects.get(pk = request.POST.get('pk'))
        np.title = request.POST.get('new_nr')
        np.save()
    if request.POST.get('remove_pdf'):
        np = NewsPapper.objects.get(pk = request.POST.get('pk'))
        if os.path.exists(os.getcwd().replace("\\", "/") + "/media/" + str(np.pdf)):
            os.remove(os.getcwd().replace("\\", "/") + "/media/" + str(np.pdf))
        np.delete()
    if request.POST.get('buy_online_premium'):
        profile = Profile.objects.get(user = request.user)
        profile.is_premium = True
        profile.save()
    if request.POST.get('buy_material_premium'):
        pass
    rendertemplate = {'np' : NewsPapper.objects.all(), "premium" : Profile.objects.get(user = request.user).is_premium}
    return render(request, 'blog/' + check_dark_theme(request) + 'online_newspapper.html', set_dict_for_render(rendertemplate, request))