from django import template

from post.models import Likes


register = template.Library()


@register.simple_tag
def get_method(post, user):
    liked = False
    like_check = Likes.objects.filter(user=user, post=post).exists()
    if like_check:
        liked = True
        return "Unlike"
    return "Like"
