from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Post, Profile, Connect, Question
from .forms import PostForm, CommentForm, ProfileForm, SignupForm, ConnectForm, QuestionForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse


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
  
  likes_posts = Post.objects.order_by('liked').reverse()
  if len(likes_posts) > 8:
    likes_posts = likes_posts[:5]

  comments_posts = Post.objects.annotate(comment_count=Count('comments')).order_by('-comment_count')
  
  context = {
  'posts':posts,
  'likes_posts':likes_posts,
  'comments_posts':comments_posts,
}
  return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
  post = get_object_or_404(Post, slug=slug)
  total_likes = post.total_likes()
  context = {
    'post':post,
    'total_likes':total_likes,
  }
  return render(request, 'blog/post_detail.html', context)

@login_required
def post_new(request, slug):
  #group of the posts will be in
  group = get_object_or_404(Connect, slug=slug)
  if request.method == "POST":
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
      post = form.save(commit=False)
      post.user = request.user
      post.published_date = timezone.now()
      post.save()
      post.connect.add(group)
      form.save_m2m()
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
      form.save_m2m()
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
  group_posts = group_profile.post.all()
  followers = group_profile.follows.all()
  user_profiles = Profile.objects.all().filter(user__in=followers)
  context = {
    'group_profile':group_profile,
    'followers':followers,
    'user_profiles':user_profiles,
    'group_posts':group_posts,
  }
  return render(request, 'blog/group_profile.html', context)

def add_group(request):
  if request.method == 'POST':
    form = ConnectForm(request.FILES, request.POST)
    if form.is_valid():
      group = form.save(commit=False)
      group.user = request.user
      group.save()
      return redirect('group_profile', slug=group.slug)
  else:
    form = ConnectForm()
    return render(request, 'blog/add_group.html', {'form':form})

def add_question(request):
  if request.method == "POST":
    form = QuestionForm(request.POST)
    if form.is_valid():
      question = form.save(commit=False)
      question.user = request.user
      question.save()
      return redirect('question_detail', pk=question.pk)
  else:
    form = QuestionForm()
    return render(request, 'blog/questionform.html', {'form':form})

def question_detail(request, pk):
  question = get_object_or_404(Question, pk=pk)
  context = {
    'question':question,
  }
  return render(request, 'blog/question_detail.html', context)

def liked_post(request, slug):
  post = get_object_or_404(Post, id=request.POST.get('post_id'))
  post.liked.add(request.user)
  return HttpResponseRedirect(reverse('post_detail', args=[str(slug)]))