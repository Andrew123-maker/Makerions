from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.conf import settings
from django.contrib.auth.models import User
from .models import Post, Profile, Connect, Question, Reply, Comment, Tag
from .forms import PostForm, CommentForm, ProfileForm, SignupForm, ConnectForm, QuestionForm, ReplyForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, DeleteView
from django.utils.decorators import method_decorator


def signup(request):
  form = SignupForm()
  if request.method == "POST":
    form = SignupForm(request.POST)
    if form.is_valid():
      user = form.save()
      
      login(request, user)
      return redirect(settings.LOGIN_REDIRECT_URL)
    
  return render(request, 'registration/signup.html', {'form':form})
    
  
def post_list(request):
  if 'BlogSearch' in request.GET:
    q = request.GET['BlogSearch']
    multiple_q = Q(Q(title__icontains=q) | Q(tag__title__icontains=q))
    try:
      posts = Post.objects.filter(multiple_q).distinct()
    except:
      posts = None
  else:
    posts = Post.objects.order_by('published_date').distinct()
  
  likes_posts = Post.objects.order_by('liked').reverse()
  if len(likes_posts) > 5:
    likes_posts = likes_posts[:5]

  comments_posts = Post.objects.annotate(comment_count=Count('comments')).order_by('-comment_count')
  if len(comments_posts) > 5:
    comment_posts = comments_posts[:5]

  tags = Tag.objects.all()
  
  context = {
  'posts':posts,
  'likes_posts':likes_posts,
  'comments_posts':comments_posts,
  'tags':tags,
}
  return render(request, 'blog/post_list.html', context)

class PostDetailView(DetailView):
  model = Post
  template_name = "blog/post_detail.html"
  context_object_name = "post"
  slug_field = 'slug'

  slug_url_kwarg = 'slug'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['total_likes'] = context['post'].total_likes()
    context['comments'] = Comment.objects.filter(post=context['post']).prefetch_related('reply_set')
    context['reply_form'] = ReplyForm()
    return context

    
@method_decorator(login_required, name="dispatch")
class PostCreateView(CreateView):
  model = Post
  form_class = PostForm
  template_name = "blog/post_edit.html"

  def form_valid(self, form):
    group_slug = self.kwargs.get('slug')
    group = get_object_or_404(Connect, slug=group_slug)
    form.instance.user = self.request.user
    self.object = form.save()
    form.instance.connect.add(group)
    return super().form_valid(form)

  def get_success_url(self):
    slug = self.object.slug
    return reverse('post_detail', args=[slug])


@method_decorator(login_required, name="dispatch")
class PostEditView(UpdateView):
  model = Post
  form_class = PostForm
  template_name = "blog/post_edit.html"

  def get_success_url(self):
    slug = self.object.slug
    return reverse('post_detail', args=[str(slug)])

class PostDeleteView(DeleteView):
  model = Post
  success_url = "/"
  
  template = "blog/post_confirm_delete.html"

@method_decorator(login_required, name="dispatch")
class CommentCreateView(CreateView):
  model = Comment
  form_class = CommentForm
  template_name = "blog/add_comment_to_post.html"
    
  def form_valid(self, form):
    self.post_slug = self.kwargs.get('slug')
    self.post = get_object_or_404(Post, slug=self.post_slug)
    form.instance.user = self.request.user
    form.instance.post = self.post
    self.object = form.save()
    return super().form_valid(form)

  def get_success_url(self):
    return reverse('post_detail', args=[str(self.post_slug)])

def view_profile(request, username):
  user = get_object_or_404(User, username=username)
  profile = Profile.objects.get(user=user)
  posts = Post.objects.filter(user=user)
  groups = Connect.objects.filter(follows=user)
  context = {
    'profile':profile,
    'posts':posts,
    'groups':groups,
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

@login_required
def follow_user(request, username):
  if request.method == "POST":
    profile = get_object_or_404(Profile, id=request.POST.get('profile_id'))
    profile.follow.add(request.user)
    return redirect('profile', username=profile.user.username)


@login_required
def reply_comment(request,slug):
  if request.method == "POST":
    post = get_object_or_404(Post, slug=slug)
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    reply_form = ReplyForm(request.POST)
    if reply_form.is_valid():
      reply = reply_form.save(commit=False)
      reply.user = request.user
      reply.comment = comment
      reply.save()
      
      return HttpResponseRedirect(reverse('post_detail', args=[str(slug)]))