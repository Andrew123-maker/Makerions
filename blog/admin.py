from django.contrib import admin
from django.contrib.auth.models import User
from .models import Post, Comment, Tag, Profile, Connect

#mix profile info into user info
class ProfileInline(admin.StackedInline):
  model = Profile
  
class UserAdmin(admin.ModelAdmin):
  model = User
  
  inlines =[ProfileInline]

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Connect)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
