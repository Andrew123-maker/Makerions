from django.contrib import admin
from django.contrib.auth.models import User
from .models import Post, Comment, Tag, Profile, Connect, Question

#mix profile info into user info
class ProfileInline(admin.StackedInline):
  model = Profile
  
class UserAdmin(admin.ModelAdmin):
  model = User
  list_display = (
    "username",
    "email",
    "first_name",
    "last_name",
    "is_staff",
    "is_active",
  )
  search_fields = ("email","username",)
  ordering = ("email","username",)
  inlines =[ProfileInline]


class ProfileAdmin(admin.ModelAdmin):
  model = Profile
  list_display = (
    "user",
    "name",
    "bio",
    "last_update",
  )
  search_fields = ("user", "name",)
  ordering = ("user",)

class PostAdmin(admin.ModelAdmin):
  model = Post

  def get_tags(self, obj):
    return ", ".join(str(tag) for tag in obj.tag.all())

  def get_likes(self, obj):
    return obj.total_likes()
    
  list_display = [
    "title",
    "user",
    "get_likes",
    "get_tags",
    "published_date",
  ]
  get_tags.short_description = "Tags"
  
  search_fields = ("user", "name",)
  ordering = ("user",)
  list_display_links = ("title",)

  
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Connect)
admin.site.register(Question)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
