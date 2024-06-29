from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Post, Profile, Connect
from .forms import PostForm, CommentForm, ProfileForm, SignupForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q

def signup(request):
  form = SignupForm()
  if request.method == "POST":
    form = SignupForm(request.POST)
    if form.is_valid():
      user = form.save()
      
      login(request, user)
      return redirect(settings.LOGIN_REDIRECT_URL)
    
  return render(request, 'registration/signup.html', context={'form':form})
  
def post_list(request):
  if 'q' in request.GET:
    q = request.GET['q']
    multiple_q = Q(Q(title__icontains=q) | Q(tag__name__icontains=q))
    posts = Post.objects.filter(multiple_q)
  else:
    posts = Post.objects.order_by('published_date').distinct()
  
  likes_posts = Post.objects.order_by('likes').reverse()
  if len(likes_posts) > 8:
    likes_posts = likes_posts[:5]

  comments_posts = Post.objects.order_by('comments')[:5]
  
  context = {
  'posts':posts,
  'likes_posts':likes_posts,
  'comments_posts':comments_posts,
}
  return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
  post = get_object_or_404(Post, slug=slug)
  context = {
    'post':post
  }
  return render(request, 'blog/post_detail.html', context)

@login_required
def post_new(request):
  if request.method == "POST":
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
      post = form.save(commit=False)
      post.user = request.user
      post.published_date = timezone.now()
      post.save()
      return redirect('post_detail', slug=post.slug)
  else:
    form = PostForm()
  return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, slug):
  post = get_object_or_404(Post, slug=slug)
  if request.method == "POST":
    form = PostForm(request.POST, request.FILES, instance=post)
    if form.is_valid():
      post = form.save(commit=False)
      post.user = request.user
      post.published_date = timezone.now()
      post.save()
      return redirect('post_detail', slug=post.slug)
  else:
    form = PostForm(instance=post)
  context = {
    'form':form,
    'post':post,
  }
  return render(request, 'blog/post_edit.html', context)

@login_required
def post_delete(request, slug):
  post = get_object_or_404(Post, slug=slug)
  post.delete()
  return redirect('post_list')

def add_comment_to_post(request, slug):
  post = get_object_or_404(Post, slug=slug)
  if request.method == "POST":
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.post = post
      comment.save()
      return redirect('post_detail', slug=post.slug)
  else:
    form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form':form})

def view_profile(request, username):
  user = get_object_or_404(User, username=username)
  profile = Profile.objects.get(user=user)
  posts = Post.objects.filter(user=user)
  context = {
    'profile':profile,
    'posts':posts,
  }
  return render(request, 'blog/profile.html', context)

def edit_profile(request, username):
  user = get_object_or_404(User, username=username)
  profile = Profile.objects.get(user=user)
  
  if request.method=="POST":
    form = ProfileForm(request.POST, request.FILES, instance=profile)
    if form.is_valid():
      profile = form.save(commit=False)
      profile.user = request.user
      profile.last_update = timezone.now()
      profile.save()
      return redirect('profile', username=profile.user)
  else:
    form = ProfileForm(instance=profile)
    context={
      'form':form
    }
    return render(request, 'blog/edit_profile.html', context)

def connect(request):
  groups = Connect.objects.all()
  context = {
    'groups':groups
  }
  return render(request, 'blog/connect.html', context)

def group_profile(request, slug):
  group_profile = get_object_or_404(Connect, slug=slug)
  followers = group_profile.follows.all()
  user_profiles = Profile.objects.all().filter(user__in=followers)
  context = {
    'group_profile':group_profile,
    'followers':followers,
    'user_profiles':user_profiles,
  }
  return render(request, 'blog/group_profile.html', context)