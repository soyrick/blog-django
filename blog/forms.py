from django import forms

from .models import Comment, Post

INPUT_CLASSES = 'w-full rounded-2xl border border-slate-700 bg-slate-950/90 px-4 py-3 text-slate-100 placeholder:text-slate-500 focus:border-slate-500 focus:outline-none focus:ring-2 focus:ring-slate-600'


class PostForm(forms.ModelForm):
    slug = forms.SlugField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Leave blank to auto-generate from title', 'class': INPUT_CLASSES}),
        help_text='Optional: leave blank to generate the slug automatically from the title.',
    )

    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'cover_image', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Share your story...', 'class': INPUT_CLASSES}),
            'title': forms.TextInput(attrs={'placeholder': 'Post title', 'class': INPUT_CLASSES}),
            'cover_image': forms.ClearableFileInput(attrs={'class': INPUT_CLASSES}),
        }


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...', 'class': INPUT_CLASSES}),
        label=''
    )

    class Meta:
        model = Comment
        fields = ['content']
