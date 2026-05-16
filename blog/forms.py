from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'cover_image', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Share your story...'}),
            'title': forms.TextInput(attrs={'placeholder': 'Post title'}),
            'slug': forms.TextInput(attrs={'placeholder': 'post-slug'}),
        }


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'}),
        label=''
    )

    class Meta:
        model = Comment
        fields = ['content']
