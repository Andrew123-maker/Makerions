from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Post, Profile
from .forms import PostForm, CommentForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q

def post_list(request):
  if 'q' in request.GET:
    q = request.GET['q']
    multiple_q = Q(tag__name__icontains=q) | Q(title__icontains=q)
    posts = Post.objects.filter(multiple_q).order_by('published_date').distinct()
  else:
    posts = Post.objects.order_by('published_date').distinct()
  context = {
    'posts':posts
  }
  return render(request, 'blog/post_list.html', context)

def post_detail(request, pk):
  post = get_object_or_404(Post, pk=pk)
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
      return redirect('post_detail', pk=post.pk)
  else:
    form = PostForm()
  return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
  post = get_object_or_404(Post, pk=pk)
  if request.method == "POST":
    form = PostForm(request.POST, request.FILES, instance=post)
    if form.is_valid():
      post = form.save(commit=False)
      post.user = request.user
      post.published_date = timezone.now()
      post.save()
      return redirect('post_detail', pk=post.pk)
  else:
    form = PostForm(instance=post)
  context = {
    'form':form,
    'post':post,
  }
  return render(request, 'blog/post_edit.html', context)

@login_required
def post_delete(request, pk):
  post = get_object_or_404(Post, pk=pk)
  post.delete()
  return redirect('post_list')

def add_comment_to_post(request, pk):
  post = get_object_or_404(Post, pk=pk)
  if request.method == "POST":
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.post = post
      comment.save()
      return redirect('post_detail', pk=post.pk)
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