from django.urls import path
from .views import inbox, directs, sendDirect, userSearch, newConversation

urlpatterns = [
    path('', inbox, name='inbox'),
    path('directs/<username>/', directs, name='directs'),
    path('send/', sendDirect, name='send_direct'),
    path('new/', userSearch, name='usersearch'),
    path('new/<username>/', newConversation, name='newconversation'),
]