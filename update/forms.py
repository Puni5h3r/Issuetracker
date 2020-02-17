from django import forms
from base.models import Issue, IssueComment, IssueLike
from django.core.validators import MinValueValidator

class IssueCloseForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['open']


class IssueCommentForm(forms.ModelForm):
    comment = forms.CharField(label='Comment',required = True, widget=forms.Textarea)
    class Meta:
        model = IssueComment
        fields = ['comment']

class IssueLikeForm(forms.ModelForm):
    class Meta:
        model = IssueLike
        fields = ['like','dislike']