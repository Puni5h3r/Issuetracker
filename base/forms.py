from django import forms

from .models import Project, ProjectAttachment, Issue, IssueAttachment, Assignees, Milestone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

import datetime

User = get_user_model()


class CreateProject(forms.ModelForm):
    #members = forms.ModelChoiceField(queryset= User.objects.all(),widget=forms.CheckboxSelectMultiple(), required=False)
    class Meta:
        model = Project
        fields = ['name', 'repository','members', 'description',]


class ProjectAttachmentForm(forms.ModelForm):
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
    weight = forms.IntegerField(required=False, validators=[MaxValueValidator(10),MinValueValidator(0)])

    class Meta:
        model = Issue
        fields = ['title','description','start_date','due_date','restrict_access','weight']

    def clean_weight(self,*args,**kwargs):
        weight = self.cleaned_data('weight')
        if weight is not None:
            if weight > 10:
                raise forms.ValidationError(_('Number must be less than 10'))
            elif weight < 0:
                raise forms.ValidationError(_('Number must be greater than 0'))
            else:
                return weight




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