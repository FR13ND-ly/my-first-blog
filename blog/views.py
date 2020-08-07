from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from datetime import timedelta
from .models import Post, Comment, Profile, Like, Survey, Vote, Ad, Image
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password

def set_dict_for_render(rdict, request):
    if 'tposts' in rdict:
       rdict.update({'tposts' : Post.objects.filter(published_date__lte=timezone.now()).order_by('count_of_views').reverse().filter(status=False)[0:3]})
    if request.user.is_active:
        profile,exist = Profile.objects.get_or_create(user = request.user)
        rdict.update({'profile':profile})
    return rdict

def check_dark_theme(request):
    if request.user.is_active:
        profile,exist = Profile.objects.get_or_create(user = request.user)
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
    rendertemplate = {'posts': posts, 'number_of_pages': number_of_pages, "bigimage": True, "current_page":1, 'tposts':True}
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
    post.count_of_views += 1
    post.save()
    user = request.user
    if user.is_active:
        liked = bool(Like.objects.filter(author=user, post=post))
    else:
        liked = False
    survey = Survey.objects.filter(post=post)
    uservoted = False
    for variant in survey:
        for i in Vote.objects.filter(variant=variant):
            if i.user == request.user:
                uservoted = True
    if request.method == "POST" and request.POST.get("add_comment"):
        comment = Comment.objects.create(post = post)
        if user.is_active:
            comment.author = user.username
            comment.photo_of_user = Profile.objects.get(user = request.user).photo
        else:
            comment.author =request.POST.get('author_of_comment')+'(neautentificat)'
        comment.text = request.POST.get('text_of_comment')
        comment.save()
        return redirect('post_detail', pk=post.pk)
    rendertemplate = {'post': post, 'user':user, 'survey': survey, 'uservoted': uservoted, "liked":liked, 'tposts':True}
    return render(request, 'blog/' + check_dark_theme(request) + 'post_detail.html', set_dict_for_render(rendertemplate, request))


@login_required
def comment_remove(request, pk):
    if not request.user.is_staff:
        return HttpResponse(status=404)
    comment = Comment.objects.get(pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def post_new(request):
    if not request.user.is_staff:
        return HttpResponse(status=404)
    if request.method == "POST" and request.POST.get("save_post"):
        post = Post.objects.create(author = request.user)
        post.title = request.POST.get("title")
        post.published_date = timezone.now()
        post.cover = request.FILES.get('coverphoto',None)
        if request.POST.get('status') == "on":
            post.status = True;
        else:
            post.status = False;
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
        post.text = request.POST.get("posttext")
        post.save()
        return redirect('post_detail', pk=post.pk)
    elif request.method == "POST":
        if request.FILES.get('file'):
            new_image = Image.objects.create(image=request.FILES.get('file'))
            new_image.save()
    rendertemplate = {"post_new": True}
    return render(request, 'blog/' + check_dark_theme(request) + 'post_edit.html', set_dict_for_render(rendertemplate, request))

@login_required
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
        post.cover = request.FILES.get('coverphoto', post.cover)
        post.text = request.POST.get("posttext", "")
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
        return redirect('post_detail', pk=post.pk)
    elif request.method == "POST" and request.POST.get("action"):
        new_image = Image.objects.create(image=request.FILES.get('file'))
        new_image.save()
    rendertemplate = {'post':post,'surveys':surveys}
    return render(request, 'blog/' + check_dark_theme(request) + 'post_edit.html', set_dict_for_render(rendertemplate, request))

@login_required
def post_remove(request, pk):
    if not request.user.is_staff:
        return HttpResponse(status=404)
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('post_list')


def user_login(request):
    if request.user.is_active:
        return redirect('post_list')
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('logininput'), password=request.POST.get('passwordinput'))
        if user is not None:
            if user.is_active:
                login(request, user)
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
                return HttpResponse('This login is taken')
        if request.POST.get('password') == request.POST.get('repeatedpassword'):
            if len(request.POST.get('password')) >5:
                user = User.objects.create(username = request.POST.get('username'), first_name = request.POST.get('firstname'), email = request.POST.get('email'))
                user.password = make_password(request.POST.get('repeatedpassword'))
                user.date_joined = timezone.now()
                user.save()
                profile = Profile.objects.create(user=user)
                profile.save()
                theuser = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
                login(request, theuser)
                return redirect('post_list')
            else:
                return HttpResponse('Password is weak')
        else:
            return HttpResponse('Passwords dont match')
    return render(request, 'blog/register.html')

def user_logout(request):
    if not request.user.is_active:
        return redirect('post_list')
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def add_like(request, pk):
    post = Post.objects.get(pk=pk)
    new_like, created = Like.objects.get_or_create(author=request.user, post=post)
    if created:
        new_like.save()
    else:
        like = Like.objects.get(author=request.user, post=post)
        like.delete()
    return redirect('post_detail', pk=post.pk)

@login_required
def vote(request,pk):
    post = Post.objects.get(pk=pk)
    survey_of_post = Survey.objects.filter(post=post)
    if post.type_of_vote:
        survey = Survey.objects.get(post = post, variant = request.POST.get('variant'))
        vote = Vote.objects.create(variant = survey, user = request.user)
        vote.save()
        survey.count = (len(Vote.objects.filter(variant= survey)));
        survey.save()
    else:
        for i in request.POST.getlist('variant'):
            survey = Survey.objects.get(post = post, variant = i)
            vote = Vote.objects.create(variant = survey, user = request.user)
            vote.save()
            survey.count = (len(Vote.objects.filter(variant= survey)));
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
        return redirect('ads')
    if request.method == "POST":
        ad = Ad.objects.create()
        ad.text = request.POST.get('ad_text')
        ad.contact = request.POST.get('contact_data')
        ad.published_date = timezone.now()
        ad.remove_date = int(request.POST.get('count_of_days'))
        ad.save()
        return redirect('ads')
    rendertemplate = {'ads_page':True, 'ad_new':True}
    return render(request, 'blog/' + check_dark_theme(request) + 'ad_edit.html', set_dict_for_render(rendertemplate, request))

def ad_edit(request, pk):
    if not request.user.is_staff:
        return redirect('ads')
    ad = Ad.objects.get(pk=pk)
    if request.method == "POST":
        ad.text = request.POST.get('ad_text')
        ad.contact = request.POST.get('contact_data')
        ad.remove_date = int(request.POST.get('count_of_days'))
        ad.save()
        return redirect('ads')
    rendertemplate = {'ads_page':True, 'ad':ad}
    return render(request, 'blog/' + check_dark_theme(request) + 'ad_edit.html', set_dict_for_render(rendertemplate, request))

def ad_delete(request, pk):
    if not request.user.is_staff:
        return redirect('ads')
    ad = Ad.objects.get(pk=pk)
    ad.delete()
    return redirect('ads')

def test_page(request):
    if request.method == "POST":
        new_image = Image.objects.create(image=request.FILES.get('file'))
        new_image.save()
    return render(request, 'blog/test.html')
