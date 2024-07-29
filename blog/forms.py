from ckeditor import widgets
from django import forms
from django.forms.widgets import ClearableFileInput, Textarea
from .models import Post, Question, Comment, Profile, Question, Connect, Reply
from django_ckeditor_5.widgets import CKEditor5Widget
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
  
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name')
      
class PostForm(forms.ModelForm):

  class Meta:
    model = Post
    fields = ('title', 'text', 'image', 'tag')

    widgets = {
      'title': forms.TextInput(attrs={'class':'form-control'}),
      'text':forms.Textarea(attrs={'class':'form-control', 'id':'editor'}),
      'image':forms.ClearableFileInput(attrs={'class':'form-control'}),
      'tag':forms.SelectMultiple(attrs={'class':'form-control'})
    }

class CommentForm(forms.ModelForm):

  class Meta:
    model = Comment
    fields = ('text',)
    
    widgets = {
      'text':forms.Textarea(attrs={'class':'form-control'}),
    }

class ProfileForm(forms.ModelForm):

  class Meta:
    model = Profile
    fields = ('name', 'bio', 'image')
  
    widgets = {
      'name':forms.TextInput(attrs={'class':'form-control'}),
      'bio':forms.Textarea(attrs={'class':'form-control', 'id':'editor'}),
      'image':forms.ClearableFileInput(attrs={'class':'form-control'}),
    }

class QuestionForm(forms.ModelForm):

  class Meta:
    model = Question
    fields = ('title', 'content')

    widgets = {
      'title':forms.TextInput(attrs={'class':'form-control'}),
      'content':forms.Textarea(attrs={'class':'form-control', 'id':'editor'}),
    }

class ConnectForm(forms.ModelForm):

  class Meta:
    model = Connect
    fields = ('title', 'description', 'image')

    widgets = {
      'title':forms.TextInput(attrs={'class':'form-control'}),
      'image':forms.ClearableFileInput(attrs={'class':'form-control'}),
      'description':forms.Textarea(attrs={'class':'form-control', 'id':'editor'}),
    }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text']
        widgets = {'text': forms.Textarea(attrs={'class': 'reply-form', 'rows': 2})}