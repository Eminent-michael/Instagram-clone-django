from pdb import post_mortem
from django.db import models
from post.models import Post
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete

from notifications.models import Notifications

# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def user_comment_post(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        sender = comment.user
        user = post.user
        
        if user != post.user:
            text_preview = comment.body[:90]
            
            notify = Notifications(post=post, sender=sender, user=user, text_preview=text_preview, notification_type=2)
            notify.save()
        
    def user_del_comment_post(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        sender = comment.user
        
        notify = Notifications.objects.filter(post=post, user=post.user, sender=sender, notification_type=2)
        notify.delete()
        
post_save.connect(Comment.user_comment_post, sender=Comment)
post_delete.connect(Comment.user_del_comment_post, sender=Comment)
        
