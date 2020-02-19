from django import forms

from .models import Project, ProjectAttachment, Issue, IssueAttachment, Assignees, Milestone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
import datetime


class CreateProject(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'repository','members', 'description',]


class ProjectAttachment(forms.ModelForm):
    class Meta:
        model = ProjectAttachment
        fields = ['image','files']


class IssueForm(forms.ModelForm):
    title = forms.CharField(label='Title', required=True)
    description = forms.CharField(label='Description',required = False, widget=forms.Textarea)
    due_date = forms.DateTimeField(initial=datetime.date.today,
                                     input_formats=['%d/%m/%Y'],
                                     widget=forms.DateTimeInput(
                                         attrs={
                                             'class': 'form-control datetimepicker-input',
                                             'data-target': '#datetimepicker2'
                                         }),required=False,
                                     )
    restrict_access = forms.BooleanField(label='Restrict access',required=False)
    weight = forms.IntegerField(
                validators=[MinValueValidator(0)],error_messages={'required':'please provide a number greater than 0'},
                required=False)

    class Meta:
        model = Issue
        fields = ['title','description','start_date','due_date','restrict_access','weight']


class IssueAttachmentForm(forms.ModelForm):
    class Meta:
        model = IssueAttachment
        fields = ['image','files']

class IssueAssigneeForm(forms.ModelForm):
    class Meta:
        model = Assignees
        fields = ['assignees']


class MilestoneForm(forms.ModelForm):
    start_date = forms.DateTimeField(initial=datetime.date.today,
                                     input_formats=['%d/%m/%Y'],
                                     widget=forms.DateTimeInput(
                                         attrs={
                                             'class': 'form-control datetimepicker-input',
                                             'data-target': '#datetimepicker3'
                                         }), required=False
                                     )
    Due_date = forms.DateTimeField(initial=datetime.date.today,
                                   input_formats=['%d/%m/%Y'],
                                   widget=forms.DateTimeInput(
                                       attrs={
                                           'class': 'form-control datetimepicker-input',
                                           'data-target': '#datetimepicker4'
                                       }), required=False,
                                   )

    class Meta:
        model = Milestone
        fields = ['title','description','start_date','Due_date']