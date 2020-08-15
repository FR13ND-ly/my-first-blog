from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from datetime import timedelta
from .models import Post, Comment, Profile, Like, Survey, Vote, Ad, Image, Tag, View
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.db.models import Count
from dateutil.relativedelta import relativedelta

def set_dict_for_render(rdict, request):
    if 'tposts' in rdict:
       rdict.update({'tposts' : Post.objects.filter(published_date__lte=timezone.now()).annotate(count_of_views = Count('view')).order_by(('count_of_views')).reverse().filter(status=False)[0:3]})
    if request.user.is_active:
        profile = Profile.objects.get_or_create(user = request.user)
        rdict.update({'profile' : profile})
    return rdict

def check_dark_theme(request):
    if request.user.is_active:
        profile, exist = Profile.objects.get_or_create(user = request.user)
        if profile.darktheme:
            return 'darktheme_'
    return ''

def post_list(request):
    if request.user.is_staff:
        relative_number_of_pages = ((len(Post.objects.filter(published_date__lte=timezone.now()))-1)//5)
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()[0:5]
    else:
        relative_number_of_pages = ((len(Post.objects.filter(published_date__lte=timezone.now()).filter(status=False))-1)//5)
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse().filter(status=False)[0:5]
    number_of_pages = []
    index = 0
    for post in posts:
        post.index = index
        index += 1
    for i in range(8):
        if 1 + i < relative_number_of_pages + 2:
            number_of_pages.append(1+i)
    rendertemplate = {'posts': posts, 'number_of_pages': number_of_pages, "current_page":1, 'tposts':True}
    return render(request, 'blog/' + check_dark_theme(request) + 'post_list.html', set_dict_for_render(rendertemplate, request))

def post_list_next(request, lk):
    if lk == 1:
        return redirect('post_list')
    if request.user.is_staff:
        relative_number_of_pages = (len(Post.objects.filter(published_date__lte=timezone.now()) )- 1)//5
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    else:
        relative_number_of_pages = (len(Post.objects.filter(published_date__lte=timezone.now()).filter(status=False))- 1)//5
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse().filter(status=False)
    if (len(posts) - lk * 5) < 0:
        posts = posts[(lk-1)*5:]
    else:
        posts = posts[(lk-1) * 5:lk * 5]
    number_of_pages = []
    for i in range(4):
        if lk-(4-i) > 0:
            number_of_pages.append(lk-(4-i))

    for i in range(4):
        if lk + i < relative_number_of_pages + 2:
            number_of_pages.append(lk+i)
    rendertemplate = {'posts': posts, 'number_of_pages': number_of_pages, "current_page":lk, 'tposts':True}
    return render(request, 'blog/' + check_dark_theme(request) + 'post_list.html', set_dict_for_render(rendertemplate, request))

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_active:
        new_view = View.objects.create(post = post, user = request.user, date = timezone.now())
    else:
        new_view = View.objects.create(post = post, date = timezone.now())
    new_view.save()
    print('new view')
    if request.user.is_active:
        liked = bool(Like.objects.filter(author=request.user, post=post))
    else:
        liked = False
    survey = Survey.objects.filter(post=post)
    uservoted = False
    for variant in survey:
        for i in Vote.objects.filter(variant=variant):
            if i.user == request.user:
                uservoted = True
    if request.method == "POST" and request.POST.get("add_comment"):
        comment = Comment.objects.create(post = post, created_date = timezone.now())
        if request.user.is_active:
            comment.author = request.user.username
            comment.photo_of_user = Profile.objects.get(user = request.user).photo
        else:
            comment.author =request.POST.get('author_of_comment') + '(neautentificat)'
        if request.user.is_staff:
            comment.by_administration = True
        comment.text = request.POST.get('text_of_comment')
        comment.save()
        print('new comment')
        return redirect('post_detail', pk=post.pk)
    rendertemplate = {'post': post, 'user':request.user, 'survey': survey, 'uservoted': uservoted, "liked":liked, 'tposts':True}
    return render(request, 'blog/' + check_dark_theme(request) + 'post_detail.html', set_dict_for_render(rendertemplate, request))


def comment_remove(request, pk):
    if not request.user.is_staff:
        return HttpResponse(status=404)
    comment = Comment.objects.get(pk=pk)
    comment.delete()
    print('comment removed')
    return redirect('post_detail', pk=comment.post.pk)

def post_new(request):
    if not request.user.is_staff:
        return HttpResponse(status=404)
    if request.method == "POST" and request.POST.get("save_post"):
        post = Post.objects.create(author = request.user, title = request.POST.get("title"), text = request.POST.get("posttext"), published_date = timezone.now())
        for i in Image.objects.all():
            if (request.POST.get("cover_name") == i.image):
                post.cover = i
        for i in request.POST.get('tags_container').split('close'):
            if i != '':
                new_tag = Tag.objects.create(tag = i, post = post)
                new_tag.save()
        if request.POST.get('survey_is_present') == "on":
            post.question = request.POST.get('survey_question')
            post.survey_is_present = True
            if request.POST.get('type_of_vote') == "on":
                post.type_of_vote = True
            else:
                post.type_of_vote = False
            for i in request.POST.getlist('variant_of_survey'):
                if i != '':
                    survey = Survey.objects.create(post=post, variant=i)
                    survey.save()
        post.save()
        print('new post')
        return redirect('post_detail', pk=post.pk)
    elif request.method == "POST" and request.FILES.get('file'):
        new_image = Image.objects.create(image=request.FILES.get('file'), upload_date = timezone.now())
        new_image.save()
        print('new image uploaded')
    rendertemplate = {"post_new": True, 'images':image_list(), "mimage_list" : Image.objects.all()}
    return render(request, 'blog/' + check_dark_theme(request) + 'post_edit.html', set_dict_for_render(rendertemplate, request))

def post_edit(request, pk):
    if not request.user.is_staff:
        return HttpResponse(status=404)
    post = Post.objects.get(pk=pk)
    surveys = dict()
    a = 0
    for i in Survey.objects.filter(post=post):
        surveys.update({i.variant:a})
        a += 1
    if request.method == "POST" and request.POST.get("save_post"):
        post.title = request.POST.get("title")
        for i in Image.objects.all():
            if (request.POST.get("cover_name") == i.image):
                post.cover = i
        post.text = request.POST.get("posttext")
        if request.POST.get('tags_container') != '':
            for tag in post.tags.all():
                tag.delete()
            for i in request.POST.get('tags_container').split('close'):
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
            for i in Survey.objects.filter(post=post):
                i.delete()
            for i in request.POST.getlist('variant_of_survey'):
                if i != '':
                    survey = Survey.objects.create(post=post, variant=i)
                    survey.save()
        else:
            post.survey_is_present = False
        post.save()
        print('post ' + post.title + ' edited')
        return redirect('post_detail', pk=post.pk)
    elif request.method == "POST" and request.FILES.get('file'):
        new_image = Image.objects.create(image=request.FILES.get('file'), upload_date = timezone.now())
        new_image.save()
        print("new image uploaded")
    rendertemplate = {'post':post,'surveys':surveys, 'images':image_list(), "mimage_list" : Image.objects.all()}
    return render(request, 'blog/' + check_dark_theme(request) + 'post_edit.html', set_dict_for_render(rendertemplate, request))

def post_remove(request, pk):
    if not request.user.is_staff:
        return HttpResponse(status=404)
    post = Post.objects.get(pk=pk).delete()
    print('post removed')
    return redirect('post_list')


def user_login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('logininput'), password=request.POST.get('passwordinput'))
        if user is not None:
            if user.is_active:
                login(request, user)
                print('somebody have login')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return render(request, 'blog/login.html', {'incorrect_login_or_password':True})
    return render(request, 'blog/login.html')

def register(request):
    if request.user.is_active:
        return redirect('post_list')
    if request.method == 'POST':
        for i in User.objects.all():
            if i.username == request.POST.get('username'):
                return render(request, 'blog/register.html', {"Error": "Acest nume de utilizator e ocupat"})
        for i in ['admin', 'administrator', '(neautentificat)', 'alan', 'estcurier', 'est-curier', 'administrația']:
            if i in request.POST.get('username').lower():
               return render(request, 'blog/register.html', {"Error": "Numele de utilizator conține un element interzis"})
        if request.POST.get('password') == request.POST.get('repeatedpassword'):
            if len(request.POST.get('password')) >5:
                user = User.objects.create(username = request.POST.get('username'), first_name = request.POST.get('firstname'), email = request.POST.get('email'), date_joined = timezone.now(), password = make_password(request.POST.get('repeatedpassword')))
                user.save()
                profile = Profile.objects.create(user=user)
                profile.save()
                theuser = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
                login(request, theuser)
                print('new user')
                return redirect('post_list')
            else:
                return render(request, 'blog/register.html', {"Error": "Parola e prea slabă"})
        else:
            return render(request, 'blog/register.html', {"Error": "Parolele nu coincid"})
    return render(request, 'blog/register.html')

def user_logout(request):
    if not request.user.is_active:
        return redirect('post_list')
    logout(request)
    print('user logout')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def add_like(request, pk):
    post = Post.objects.get(pk=pk)
    new_like, created = Like.objects.get_or_create(author=request.user, post=post)
    if created:
        new_like.date = timezone.now()
        new_like.save()
        print('new like')
    else:
        like = Like.objects.get(author=request.user, post=post)
        like.delete()
        print('like removed')
    return redirect('post_detail', pk=post.pk)

@login_required
def vote(request,pk):
    post = Post.objects.get(pk=pk)
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
            survey.count = (len(Vote.objects.filter(variant= survey)))
            survey.save()
    return redirect('post_detail', pk=pk)

@login_required
def setusertheme(request, theme):
    profile = Profile.objects.get(user = request.user)
    profile.darktheme = bool(theme)
    profile.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def ads_list(request):
    for i in Ad.objects.all():
        if timedelta(days=7 * i.remove_date) + i.published_date < timezone.now():
            i.delete()
    ads = dict()
    a = 1
    for i in Ad.objects.all():
        if a == 4:
            a = 1
        ads.update({i:a})
        a += 1
    first_column, second_column, third_column = [], [], []
    for i in ads:
        if ads[i] == 1:
            first_column.append(i)
        if ads[i] == 2:
            second_column.append(i)
        if ads[i] == 3:
            third_column.append(i)
    ads = [first_column, second_column, third_column]
    ads_for_mobile = Ad.objects.all()
    rendertemplate = {'ads_page':True, 'ads_list':True, 'ads': ads, 'mads': ads_for_mobile}
    return render(request, 'blog/' + check_dark_theme(request) + 'ads.html',set_dict_for_render(rendertemplate, request))

def ad_new(request):
    if not request.user.is_staff:
        return HttpResponse(status=404)
    if request.method == "POST":
        ad = Ad.objects.create(text = request.POST.get('ad_text'), contact = request.POST.get('contact_data'), published_date = timezone.now(), remove_date = int(request.POST.get('count_of_days')))
        ad.save()
        print('new ad')
        return redirect('ads')
    rendertemplate = {'ads_page':True, 'ad_new':True}
    return render(request, 'blog/' + check_dark_theme(request) + 'ad_edit.html', set_dict_for_render(rendertemplate, request))

def ad_edit(request, pk):
    if not request.user.is_staff:
        return HttpResponse(status=404)
    ad = Ad.objects.get(pk=pk)
    if request.method == "POST":
        ad.text = request.POST.get('ad_text')
        ad.contact = request.POST.get('contact_data')
        ad.remove_date = int(request.POST.get('count_of_days'))
        ad.save()
        print('ad edited')
        return redirect('ads')
    rendertemplate = {'ads_page':True, 'ad':ad}
    return render(request, 'blog/' + check_dark_theme(request) + 'ad_edit.html', set_dict_for_render(rendertemplate, request))

def ad_delete(request, pk):
    if not request.user.is_staff:
        return HttpResponse(status=404)
    ad = Ad.objects.get(pk=pk)
    ad.delete()
    print('ad deleted')
    return redirect('ads')

def image_list():
    imgs = dict()
    a = 1
    for i in Image.objects.all().order_by("upload_date").reverse():
        if a == 4:
            a = 1
        imgs.update({i:a})
        a += 1
    first_column, second_column, third_column = [], [], []
    for i in imgs:
        if imgs[i] == 1:
            first_column.append(i)
        if imgs[i] == 2:
            second_column.append(i)
        if imgs[i] == 3:
            third_column.append(i)
    images = [first_column, second_column, third_column]
    return images

def test_page(request):
    return render(request, 'blog/test.html', set_dict_for_render(rendertemplate, request))

def prepare(word):
    return word.lower().replace('ț', 't').replace('ș', 's').replace('î', 'i').replace('â', 'a').replace('ă', 'a')

def prepare_word_list(word_list):
    for i in ["și", "sau", "de", "care", "la", "a", "fi", "eu", "ea", "el", "dar", "tu"]:
        if i in word_list:
            word_list.remove(i)
    return word_list

def search(request):
    words_list = prepare_word_list(request.GET.get('search').split(' '))
    posts = []
    ads = []
    comments = []
    for word in words_list:
        for post in Post.objects.all().order_by("published_date").reverse():
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
        for comment in Comment.objects.all().order_by("created_date").reverse():
                for word_of_comment in prepare_word_list(ad.text.split(" ")):
                    if prepare(word_of_comment) == prepare(word) and comment not in comments:
                        comments.append(comment)
    rendertemplate = {"posts":posts, "ads":ads, "comments":comments, "search_page": True}
    return render(request, 'blog/' + check_dark_theme(request) + 'search_page.html', set_dict_for_render(rendertemplate, request))

def search_by_teg(request, tag):
    posts = []
    for post in Post.objects.all().order_by("published_date").reverse():
        if not post in posts:
            for post_tag in post.tags.all():
                if post_tag.tag.lower() == tag.lower():
                    posts.append(post)
    rendertemplate = {"posts":posts, 'hide_ads_and_comments':True}
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
    for i in range(int(timezone.now().strftime("%d")), -1, -1):
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
        if "(neautentificat)" in i.author:
            comment_by_signed_and_not["Oaspeți"] += 1
        else:
            comment_by_signed_and_not["Autentificați"] += 1
    rendertemplate = {"Administrators":Administrators, "Users": Users, "Posts":Posts, "Views":Views, "Likes": Likes, "Comments": Comments, "views_by_date" : views_by_date, "views_by_month": views_by_month, "views_by_year": views_by_year, 'views_by_signed_and_not': views_by_signed_and_not , "white_or_dark_theme_stat":white_or_dark_theme_stat, "comment_by_signed_and_not" : comment_by_signed_and_not}
    return render(request, 'blog/' + check_dark_theme(request) + 'statistic.html', set_dict_for_render(rendertemplate, request))