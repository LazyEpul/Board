from django.db import models
from boards.models import Post, Board, Topic
from django import forms
from django.db.models import fields

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'What is on your mind?'}), max_length=4000)

    class Meta:
        model = Topic
        fields = ['subject','message']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message']