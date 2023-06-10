from django.urls import path
from .view_api import LikeViewApi

urlpatterns = [
    path("like", LikeViewApi.as_view(), name="like_view"),
]
