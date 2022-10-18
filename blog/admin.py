from django.contrib import admin

# Register your models here.
from blog.models import Category, Post, Comment, Profile

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)