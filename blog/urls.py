from django.urls import path
from . import views

urlpatterns = [
  path('', views.post_list, name="post_list"),
  path('post/<str:slug>', views.PostDetailView.as_view(), name="post_detail"),
  path('<str:slug>/post/new/', views.PostCreateView.as_view(), name="post_new"),
  path('post/<str:slug>/edit/', views.PostEditView.as_view(), name='post_edit'),
  path('post/<str:slug>/delete', views.PostDeleteView.as_view(), name="post_delete"),
  path('post/<str:slug>/comment', views.CommentCreateView.as_view(), name="add_comment_to_post"),
  path('<str:username>/profile', views.view_profile, name="profile"),
  path('edit/<str:username>/profile', views.edit_profile, name='edit_profile'),
  path('group/', views.connect, name="connect"),
  path('group/<str:slug>/profile', views.group_profile, name="group_profile"),
  path('follow/<str:username>/', views.follow_user, name="follow_user"),
  path('add/group/', views.add_group, name="add_group"),
  path('add/question/', views.add_question, name="add_question"),
  path('question/<int:pk>/detail', views.question_detail, name="question_detail"),
  path('liked/<str:slug>', views.liked_post, name="liked_post"),
  path('<str:slug>/comment/reply/', views.reply_comment, name="reply"),
]