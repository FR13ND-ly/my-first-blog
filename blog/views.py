from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Post, Comment, Profile, Like, Survey, Vote, Ad, Image
from django.http import HttpResponse
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password

def set_dict_for_render(rdict, request):
    rdict.update({'tposts' : Post.objects.filter(published_date__lte=timezone.now()).order_by('count_of_views').reverse().filter(status=False)[0:3]})
    if request.user.is_active:
        profile = Profile.objects.get(user = request.user)
        rdict.update({'profile':profile})
    return rdict
    

def post_list(request):
    if request.user.is_staff:
        relative_number_of_pages = (len(Post.objects.filter(published_date__lte=timezone.now()))//5)
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()[0:5]
    else:
        relative_number_of_pages = (len(Post.objects.filter(published_date__lte=timezone.now()).filter(status=False))//5)
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse().filter(status=False)[0:5]
    number_of_pages = []
    index = 0
    for post in posts:
        post.index = index
        index += 1
    for i in range(8):
        if 1 + i < relative_number_of_pages + 2:
            number_of_pages.append(1+i)
    rendertemplate = {'posts': posts, 'number_of_pages': number_of_pages, "bigimage": True, "current_page":1}
    return render(request, 'blog/post_list.html', set_dict_for_render(rendertemplate, request))

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
    print(lk)
    rendertemplate = {'posts': posts, 'number_of_pages': number_of_pages, "current_page":lk}
    return render(request, 'blog/post_list.html', set_dict_for_render(rendertemplate, request))

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
    if request.method == "POST":
        if request.POST.get("add_comment"):
            comment = Comment.objects.create(post = post)
            if user.is_active:
                comment.author = user.username
                comment.photo_of_user = Profile.objects.get(user = request.user).photo
            else:
                comment.author =request.POST.get('author_of_comment')
            comment.text = request.POST.get('text_of_comment')
            comment.save()
            return redirect('post_detail', pk=post.pk)
    rendertemplate = {'post': post, 'user':user, 'survey': survey, 'uservoted': uservoted, "liked":liked}
    return render(request, 'blog/post_detail.html', set_dict_for_render(rendertemplate, request))


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
    if request.method == "POST":
        if request.POST.get("mybtn"):
            image = Image.objects.create(image = request.FILES.get('inpostphoto'))
            if request.POST.get('status') == "on":
                status = True;
            else:
                status = False;
            rendertemplate = {"post_new": True, 'post_cover':request.FILES.get('coverphoto'), 'post_text':request.POST.get("posttext"), "post_title":request.POST.get("title"), 'post_status':status}
            return render(request, 'blog/post_edit.html', set_dict_for_render(rendertemplate, request))
        else: 
            if request.POST.get("save_post"):
                post = Post.objects.create(author = request.user)
                post.title = request.POST.get("title", "Fără Titlu")
                post.published_date = timezone.now()
                post.cover = request.FILES.get('coverphoto')
                if request.POST.get('status') == "on":
                    post.status = True;
                else:
                    post.status = False;
                post.text = request.POST.get("posttext")
                post.question = request.POST.get("question")
                post.save()
                return redirect('post_detail', pk=post.pk)
    rendertemplate = {"post_new": True}
    return render(request, 'blog/post_edit.html', set_dict_for_render(rendertemplate, request))

@login_required
def post_edit(request, pk):
    if not request.user.is_staff:
        return HttpResponse(status=404)
    post = Post.objects.get(pk=pk)
    surveys = dict()
    a = 1
    for i in Survey.objects.filter(post=post):
        surveys.update({i.variant:a})
        a += 1
    if request.method == "POST":
        if request.POST.get("mybtn"):
            image = Image.objects.create(image = request.FILES.get('inpostphoto'))
            if request.POST.get('status') == "on":
                status = True;
            else:
                status = False;
            rendertemplate = {"post_new": True, 'post_cover':request.FILES.get('coverphoto', post.cover), 'post_text':request.POST.get("posttext"), "post_title":request.POST.get("title"), 'post_status':status}
            return render(request, 'blog/post_edit.html', set_dict_for_render(rendertemplate, request))
        else: 
            if request.POST.get("save_post"):
                post.title = request.POST.get("title", "Fără Titlu")
                post.author = request.user
                post.cover = request.FILES.get('coverphoto', post.cover)
                post.text = request.POST.get("posttext", "")
                a = 1
                nowadaysvariants = []
                while a < int(request.POST.get("numberofvariants"))+1:
                    if request.POST.get("textofvariant" + str(a)) != None:
                        survey, exist = Survey.objects.get_or_create(post=post, variant = request.POST.get("textofvariant" + str(a)))
                        if request.POST.get("typeofcheck") == 'radio':
                            survey.typeofvote = True
                        elif request.POST.get("typeofcheck") == "checkbox":
                            survey.typeofvote = False
                        survey.save()
                    nowadaysvariants.append(survey)
                    a +=1
                for i in Survey.objects.filter(post = post):
                    if i not in nowadaysvariants:
                        i.delete()
                post.question = request.POST.get("question")
                if request.POST.get('status') == "on":
                    post.status = True;
                else:
                    post.status = False;
                post.save()
                return redirect('post_detail', pk=post.pk)
    rendertemplate = {'post_cover':post.cover, 'post_question':post.question, "post_text":post.text, "post_status" :post.status,'post_title':post.title,'surveys': surveys,'surveytype':Survey.objects.filter(post=post)[0].typeofvote}
    return render(request, 'blog/post_edit.html', set_dict_for_render(rendertemplate, request))

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
                return redirect('post_list')
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
                profile.photo = request.FILES.get('userphoto')
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
    logout(request)
    return redirect('post_list')

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
    surveyofpost = Survey.objects.filter(post=post)
    if surveyofpost[0].typeofvote:
        survey = Survey.objects.get(post = post, variant = request.GET.get('value'))
        vote = Vote.objects.create(variant = survey, user = request.user)
        survey.count = (len(Vote.objects.filter(variant= survey)))
        survey.save()
        vote.save()
    else:
        for i in surveyofpost:
            if request.GET.get(i.variant) == 'on':
                survey = Survey.objects.get(post = post, variant = i.variant)
                vote = Vote.objects.create(variant = survey, user = request.user)
                survey.count = (len(Vote.objects.filter(variant= survey)))
                survey.save()
                vote.save()
    return redirect('post_detail', pk=pk)

@login_required
def setusertheme(request, theme):
    profile = Profile.objects.get(user = request.user)
    profile.darktheme = bool(theme)
    profile.save()
    return redirect('post_list')

def ads_list(request):
    for i in Ad.objects.all():
        if timedelta(days=7*i.remove_date) + i.published_date < timezone.now():
            i.delete()
    return render(request, 'blog/ads.html', {'ads_page':True, 'ads': Ad.objects.all()})

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
    return render(request, 'blog/ad_edit.html', {'ads_page':True, 'ad_new':True})

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
    return render(request, 'blog/ad_edit.html', {'ads_page':True, 'ad':ad})

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