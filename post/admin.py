from django.contrib import admin
from post.models import *
# Register your models here.

admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Tag)
admin.site.register(Stream)
admin.site.register(Likes)


