from django import forms
from django.forms.widgets import ClearableFileInput, Textarea
from .models import Post, Tag, Comment, Profile
from ckeditor.widgets import CKEditorWidget

class PostForm(forms.ModelForm):
  
  class Meta:
    model = Post
    tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.SelectMultiple(attrs={'class':'form-control'}))
    
    fields = ("image", 'title', 'tag', 'text', 'likes')
    
    widgets = {
    'image':forms.ClearableFileInput(attrs={'class':'form-control'}),
    'title': forms.TextInput(attrs={'class':'form-control'}),
    'text':forms.Textarea(attrs={'class':'form-control', 'id':'editor'})
  }

class CommentForm(forms.ModelForm):

  class Meta:
    model = Comment
    fields = ('user','text')
    
    widgets = {
      'user':forms.TextInput(attrs={'class':'form-control'}),
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
  