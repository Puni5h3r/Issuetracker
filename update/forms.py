from django import forms

from base.models import Issue, IssueComment, IssueLike
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _
from base.models import Assignees, Label
from base.widgets import ColorPickerWidget

class IssueCloseForm(forms.ModelForm):
    weight = forms.IntegerField(
        validators=[MinValueValidator(0, _('Must be zero or greater than zero'))],
        required=False)

    class Meta:
        model = Issue
        fields = ['open','weight']


class IssueCommentForm(forms.ModelForm):
    comment = forms.CharField(label='Comment',required = True, widget=forms.Textarea)
    class Meta:
        model = IssueComment
        fields = ['comment']

class IssueLikeForm(forms.ModelForm):
    class Meta:
        model = IssueLike
        fields = ['like','dislike']


class AddAssigneeForm(forms.ModelForm):

    class Meta:
        model = Assignees
        fields = ['assignees','access']


class LabelFrom(forms.ModelForm):
    color_label = forms.CharField(widget=ColorPickerWidget)
    class Meta:
        model = Label
        fields = ['color_label','priority']