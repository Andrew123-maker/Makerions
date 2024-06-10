from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import SlugField
from django.utils.text import slugify 
import uuid
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django_ckeditor_5.fields import CKEditor5Field

# uploading user files to a specific directory
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user, filename)
  
class Tag(models.Model):
  name = models.CharField(max_length=30)
  slug = SlugField(null=False, unique=True, default=uuid.uuid1)
  
  def get_absolute_url(self):
    return reverse('tag', args=[self.slug])
    
  def save(self, *arg, **kwargs):
    if not self.slug:
      self.slug = slugify(self.slug)
    return super().save(*arg, **kwargs)
    
  def __str__(self):
    return self.name
    
class Post(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  image = models.ImageField(blank=True, null=True, upload_to=user_directory_path)
  title = models.CharField(max_length=200)
  text = CKEditor5Field('Text', config_name="extends", blank=True)
  tag = models.ManyToManyField(Tag, related_name="tag")
  likes = models.IntegerField(default = 0)
  published_date = models.DateTimeField(blank=True, null=True, auto_now=True)
  
  def __str__(self):
    return self.title

class Comment(models.Model):
  user = models.CharField(max_length=50)
  post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name="comments")
  text = models.TextField()
  created_date = models.DateTimeField(default=timezone.now)
  likes = models.IntegerField(default=0)
  
  def __str__(self):
    return self.text

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  bio = CKEditor5Field(config_name="extends", blank=True, null=True)
  image = models.ImageField(default='default.jpg',upload_to=user_directory_path)
  follows = models.ManyToManyField('self', related_name="following", symmetrical=False, blank=True)
  last_update = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.user.username

  
