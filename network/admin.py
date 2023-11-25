from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Comment

# Register your models here.
UserAdmin.fieldsets +=  ('Bio', {'fields': ('bio',)}), ('Profile photo', {'fields': ('profile_photo',)}), ('Followers', {'fields': ('followers',)}), ('Following', {'fields': ('following',)}), ('Posts', {'fields': ('posts',)}),

admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Comment)

