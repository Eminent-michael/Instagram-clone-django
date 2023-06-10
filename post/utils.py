from .models import Likes
from authy.models import Profile


def like_and_favorite(request, post_id):
    favorited = False
    liked = False
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        if profile.favorites.filter(id=post_id).exists():
           favorited = True 
        if Likes.objects.filter(user=request.user, post=post_id).exists():
            liked = True
    return liked, favorited
           