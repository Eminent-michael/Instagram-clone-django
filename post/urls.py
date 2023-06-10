from post.views import index, newPost, PostDetails, tags, like, favorite
from django.urls import path, include

urlpatterns = [
    path('', index, name='index'),
    path('newpost/', newPost, name='newpost'),
    path('<uuid:post_id>', PostDetails, name='postdetails'),
    path('tag/<str:tag_title>', tags, name='tags'),
    path('like', like, name='postlike'),
    path('<uuid:post_id>/favorite', favorite, name='favorite'),
    path("api/", include("post.urls_api")),
]