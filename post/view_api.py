from rest_framework.response import Response
from rest_framework import generics

# Models imports
from .models import Post


class LikeViewApi(generics.ListAPIView):
    queryset = Post.objects.all()
    