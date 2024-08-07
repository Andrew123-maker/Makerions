from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import SlugField
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField
import uuid
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import pre_save
from django_ckeditor_5.fields import CKEditor5Field
from blog.utils import unique_slug_generator

# uploading user files to a specific directory
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user, filename)
  
class Tag(models.Model):
  title = models.CharField(max_length=30)
  slug = SlugField(null=False, unique=True, default=uuid.uuid1)
  
  def get_absolute_url(self):
    return reverse('tag', args=[self.slug])
    
  def __str__(self):
    return self.title
    
class Post(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  slug = SlugField(max_length=150, blank=True)
  image = models.ImageField(blank=True, null=True, upload_to=user_directory_path)
  title = models.CharField(max_length=200)
  text = CKEditor5Field('Text', config_name="extends", blank=True)
  tag = models.ManyToManyField(Tag, related_name="tag")
  liked = models.ManyToManyField(User, related_name="liked")
  published_date = models.DateTimeField(blank=True, null=True, auto_now=True)
  connect = models.ManyToManyField('Connect', blank=True, related_name="posts_group")

  def get_absolute_url(self):
    return reverse('post_detail', args=[self.slug])

  def total_likes(self):
    return self.liked.count()
    
  def __str__(self):
    return self.title


class Comment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name="comments")
  text = models.TextField()
  created_date = models.DateTimeField(default=timezone.now)
  likes = models.IntegerField(default=0)
  
  def __str__(self):
    return self.text
    
class Reply(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
  text = models.CharField(max_length=150)
  published_date = models.DateTimeField(blank=True, null=True, auto_now=True)

  class Meta:
    ordering = ['-published_date']

  def __str__(self):
    return self.text

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  follow = models.ManyToManyField(User, related_name="follow")
  name = models.CharField(max_length=50)
  bio = CKEditor5Field(config_name="extends", blank=True, null=True)
  image = models.ImageField(default='default.jpg',upload_to=user_directory_path)
  last_update = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.user.username

class Question(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=150)
  content = CKEditor5Field(config_name="extends", blank=True)

  def __str__(self):
    return self.title

class Connect(models.Model):
  user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
  title = models.CharField(max_length=100, unique=True, default=None)
  slug = SlugField(max_length=150, blank=True)
  follows = models.ManyToManyField(User, related_name="following", blank=True)
  description = CKEditor5Field('Description', config_name="extends", blank=True, null=True)
  post = models.ManyToManyField(Post, related_name="group_posts",blank=True)
  image = models.ImageField(blank=True, null=True, upload_to=user_directory_path)
  question = models.ManyToManyField(Question, default=None)

  def get_absolute_url(self):
    return reverse('group_profile', args=[self.slug])

  def __str__(self):
    return self.title


def slug_generator(sender,instance, *arg, **kwargs):
  if not instance.slug:
    instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Post)
pre_save.connect(slug_generator, sender=Connect)
  
