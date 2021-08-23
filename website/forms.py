from website.models import Media, Post
from django import forms
from users.models import Profile

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['title', 'media', 'description']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']