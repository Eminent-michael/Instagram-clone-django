import uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.urls import reverse
from django.utils.text import slugify

# Models
from notifications.models import Notifications


# Create your models here.

def user_directory_path(instance, filename):
    # this file will be uploaded to MEDIA_ROOT /user(id)/filename
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Tag(models.Model):
    title = models.CharField(max_length=75, verbose_name='Tag')
    # slug = models.SlugField(null=True, blank=True, unique=True)

    class Meta:
        verbose_name_plural = 'Tags'

    def get_absolute_url(self):
        return reverse("tags", args=[self.title])

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     return super().save(*args, **kwargs)


class PostFileContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_user')
    file = models.FileField(upload_to=user_directory_path)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.ManyToManyField(PostFileContent, related_name='contents')
    caption = models.TextField(max_length=1500, null=True, blank=True, verbose_name="Caption")
    posted = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='tags')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse("postdetails", args={str(self.id)})  # type: ignore
    

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower') # People following you are followers.
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following') # following is Me
    
    def user_follow(sender, instance, *args, **kwargs): # type: ignore
        follow = instance
        sender = follow.follower
        following = follow.following
        notify = Notifications(sender=sender, user=following, notification_type=3)
        notify.save()
        
    def user_unfollow(sender, instance, *args, **kwargs): # type: ignore
        follow = instance
        sender = follow.follower
        following = follow.following
        notify = Notifications.objects.filter(sender=sender, user=following, notification_type=3)
        notify.delete()


class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs): # type: ignore
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date=post.posted, following=user)
            stream.save()


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    
    def user_liked_post(sender, instance, *args, **kwargs): # type: ignore
        like = instance
        post = like.post
        sender = like.user
        if sender != post.user:
            notify = Notifications(post=post, sender=sender,user=post.user, notification_type=1)
            notify.save()

    def user_unliked_post(sender, instance, *args, **kwargs): # type: ignore
        like = instance
        post = like.post
        sender = like.user
        notify = Notifications.objects.filter(post=post, sender=sender, notification_type=1)
        notify.delete()

# Stream
post_save.connect(Stream.add_post, sender=Post)

# Like
post_save.connect(Likes.user_liked_post, sender=Likes)
post_delete.connect(Likes.user_unliked_post, sender=Likes)

# Follow
post_save.connect(Follow.user_follow, sender=Follow)
post_delete.connect(Follow.user_unfollow, sender=Follow)
