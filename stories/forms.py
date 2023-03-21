from django import forms
from .models import Story, Category, Tag, Comment
from simplemde.widgets import SimpleMDEEditor


class StoryForm(forms.ModelForm):
    text = forms.CharField(widget=SimpleMDEEditor())

    class Meta:
        model = Story
        fields = ['title', 'url', 'text', 'category', 'tags']

    def __init__(self, *args, **kwargs):
        super(StoryForm, self).__init__(*args, **kwargs)
        self.fields['tags'].widget = forms.CheckboxSelectMultiple()
        self.fields['tags'].queryset = Tag.objects.all()


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']


class CommentForm(forms.ModelForm):
    parent_comment = forms.ModelChoiceField(
        queryset=Comment.objects.all(), required=False, widget=forms.HiddenInput
    )

    class Meta:
        model = Comment
        fields = ['text', 'parent_comment']
