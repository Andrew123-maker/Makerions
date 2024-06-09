from ckeditor import widgets
from django import forms
from django.forms.widgets import ClearableFileInput, Textarea
from .models import Post, Tag, Comment, Profile
from django_ckeditor_5.widgets import CKEditor5Widget
class PostForm(forms.ModelForm):

  class Meta:
    model = Post
    exclude = ('likes', 'user', 'published_date')

    widgets = {
      'image':forms.ClearableFileInput(attrs={'class':'form-control'}),
      'title': forms.TextInput(attrs={'class':'form-control'}),
        'text':forms.Textarea(attrs={'class':'form-control', 'id':'editor'}),
      'tag':forms.SelectMultiple(attrs={'class':'form-control'})
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
  