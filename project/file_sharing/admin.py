from django.contrib import admin
from .models import File, Comment, Review, CustomUser

admin.site.register(File)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(CustomUser)
