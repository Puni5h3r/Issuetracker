from django import forms

from base.models import Issue, IssueComment, IssueLike, Label
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _
from base.models import Assignees
from django.forms.widgets import TextInput
from django.contrib.auth import get_user_model
from .tasks import *

User = get_user_model()


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

    def send_email(self,email,issue,current_site):
        subject = 'There has been an issue in the project: {}'.format(issue.project.name)
        body = "Hi,\n You have been assigned to the following project as there has been an issue. Link on the link below to go to the following issue."
        body = body+"\n http://"+str(current_site.domain)+"/projects/{}/issue/update/".format(str(issue.id))
        send_email_task.delay(
            email,subject,body)


class LabelFrom(forms.ModelForm):
    class Meta:
        model = Label
        widgets ={
                   'color_label': TextInput(attrs={'type': 'color'}),
                   }
        fields = ['color_label','priority']