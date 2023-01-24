from django import forms
from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    class Meta(ModelForm):
        model = Post
        fields = ('text', 'group')
        group = forms.ModelChoiceField(
            queryset=Post.objects.all(),
            required=False,
            to_field_name='group'
        )
