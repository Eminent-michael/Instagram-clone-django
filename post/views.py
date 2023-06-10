from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

# Models:
from post.models import Post, Stream, Tag, Likes, PostFileContent
from authy.models import Profile
from comment.models import Comment
from post.utils import like_and_favorite
from stories.models import Story, StoryStream

# Forms:
from post.form import NewPostForm
from comment.forms import commentForm


# Create your views here.

@login_required
def index(request):
    user = request.user
    posts = Stream.objects.filter(user=user).order_by("-post")
    stories = StoryStream.objects.filter(user=user)

    group_ids = []

    for post in posts:
        group_ids.append(post.post_id)

    post_items = Post.objects.filter(
        id__in=group_ids).all().order_by('-posted')
    

    template = loader.get_template('home.html')

    context = {
        'post_items': post_items,
        'stories': stories,
        }

    return HttpResponse(template.render(context, request))


@login_required
def PostDetails(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    favorited = False

    # comments
    comments = Comment.objects.filter(post=post_id).order_by('date')

    # comments form
    if request.method == "POST":
        form = commentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('postdetails', args=[post_id]))
    else:
        form = commentForm()

    liked, favorited = like_and_favorite(request, post_id)
    template = loader.get_template('post_detail.html')

    context = {
        'post': post,
        'favorited': favorited,
        'liked': liked,
        'comments': comments,
        'form': form,
    }

    return HttpResponse(template.render(context, request))


@login_required
def newPost(request):
    user = request.user.id
    tags_objs = []
    file_objs = []

    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('content')
            caption = form.cleaned_data.get('caption')
            tags_form = form.cleaned_data.get('tags')

            tags_list = list(tags_form.replace(" ", "").split(','))

            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)

            for file in files:
                file_instance = PostFileContent(user=request.user, file=file)
                file_instance.save()
                file_objs.append(file_instance)

            p, created = Post.objects.get_or_create(
                caption=caption, user_id=user)
            p.tags.set(tags_objs)
            p.content.set(file_objs)
            p.save()

            return redirect('index')
    else:
        form = NewPostForm()

    context = {'form': form}
    return render(request, 'newpost.html', context)


@login_required
def tags(request, tag_title):
    tags = Tag.objects.filter(title__iexact=tag_title).all()
    tag_list = []
    for tag in tags:
        tag_list.append(tag)
        
    posts = Post.objects.filter(tags__in=tag_list).all().order_by('-posted')

    template = loader.get_template('tag.html')
    context = {'posts': posts, 'tag': tag}

    return HttpResponse(template.render(context, request))


@login_required
def like(request):
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post = Post.objects.get(id=post_id)
        current_like = post.likes
        
        Liked = Likes.objects.filter(user=user, post=post).count()
        
        if not Liked:
            Likes.objects.create(user=user, post=post)
            current_like += 1
        else:
            Likes.objects.get(user=user, post=post).delete()
            current_like -= 1
        post.likes = current_like
        post.save()
    
    return JsonResponse({"likes":post.likes}, safe=False)
    
    return HttpResponseRedirect(reverse("postdetails", args=[post_id]))


def favorite(request, post_id):
    user = request.user
    profile = Profile.objects.get(user=user)
    post = Post.objects.get(id=post_id)

    if profile.favorites.filter(id=post_id).exists():
        profile.favorites.remove(post)
    else:
        profile.favorites.add(post)

    return HttpResponseRedirect(reverse('postdetails', args=[post_id]))
