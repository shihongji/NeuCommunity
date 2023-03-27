from django import forms
from .models import Story, Category, Comment
from simplemde.widgets import SimpleMDEEditor


class StoryForm(forms.ModelForm):
    # text = forms.CharField(widget=forms.Textarea(attrs={'rows': 20}))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), empty_label="Select a category (required)")

    class Meta:
        model = Story
        fields = ['title', 'url', 'text', 'category', 'tags_new']

    # def __init__(self, *args, **kwargs):
    #     super(StoryForm, self).__init__(*args, **kwargs)
    #     self.fields['tags'].widget = forms.CheckboxSelectMultiple()
    #     self.fields['tags'].queryset = Tag.objects.all()

# I integrage these above.
# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ['name']
#
#
# class TagForm(forms.ModelForm):
#     class Meta:
#         model = Tag
#         fields = ['name']


class CommentForm(forms.ModelForm):
    parent_comment = forms.ModelChoiceField(
        queryset=Comment.objects.all(), required=False, widget=forms.HiddenInput
    )

    class Meta:
        model = Comment
        fields = ['text', 'parent_comment']
