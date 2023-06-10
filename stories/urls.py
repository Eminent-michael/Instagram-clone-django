from django.urls import path
from .views import newStory, showMedia

urlpatterns = [
    path('newstory/', newStory, name='newstory'),
    path('showmedia/<story_id>', showMedia, name='showmedia'),
]