from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.db.models import Q
from django.template.context_processors import csrf
from django.shortcuts import redirect, reverse

from .forms import CreateProject, ProjectAttachment, IssueForm, IssueAttachmentForm, IssueAssigneeForm, MilestoneForm
from .models import Project, Issue, Assignees


class ProjectList(ListView):
    template_name = 'projects/project_index.html'
    paginate_by = 100

    def get_queryset(self):
        return Project.objects.filter(Q(created_by_user= self.request.user) | Q(members= self.request.user)).order_by('created_on')


def new_project(request):
    project_form = CreateProject
    attachment_form = ProjectAttachment
    context = {}
    context.update(csrf(request))
    context ['project_form'] = project_form
    context ['attachment_form'] = attachment_form


    if request.method == 'POST':
        form1 = project_form(request.POST or None)
        form2 = attachment_form(request.POST or None)
        if form1.is_valid() and form2.is_valid():
            project = form1.save(commit=False)
            members = request.POST.get('members' or None)
            project.created_by_user = request.user
            project.updated_by_user = request.user
            project.save()
            for id in members:
                project.members.add(id)
            attachment = form2.save(commit=False)
            attachment.project = project
            attachment.save()
            return redirect('base:Project')

        elif form1.is_valid():
            project = form1.save(commit=False)
            project.created_by_user = request.user
            project.updated_by_user = request.user
            project.save()
            return redirect('base:Project')

    return render(request, 'projects/create_project_template.html', context)


def project_detail(request, id):
    project = Project.objects.get(pk = id)
    issue = Issue.objects.filter(project__project_id=id)
    context = {}
    context ['project'] = project
    context['issue'] = issue
    return render(request,'projects/project_detail.html',context)



def create_issue(request, id):
    project = Project.objects.get(pk=id)
    issue_form = IssueForm
    attachment_form = IssueAttachmentForm
    assignee_form = IssueAssigneeForm
    milestone_form = MilestoneForm
    context = {}
    context.update(csrf(request))
    context ['issue_form'] = issue_form
    context ['attachment_form'] = attachment_form
    context ['assinee_form'] = IssueAssigneeForm
    context ['milestone_form'] = MilestoneForm
    context ['project'] = project

    if request.method == 'POST':
        form1 = issue_form(request.POST or None)
        form2 = attachment_form(request.POST or None)
        form3 = assignee_form(request.POST or None)
        form4 = milestone_form(request.POST or None)

        if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
            issue = form1.save(commit=False)
            issue.project = project
            issue.created_by_user = request.user
            issue.updated_by_user = request.user
            issue.save()
            attachment = form2.save(commit=False)
            attachment.issue = issue
            attachment.updated_by_user = request.user
            attachment.save()
            assignee = form3.save(commit=False)
            assignee.issue = issue
            assignee.save()
            assignees_members = request.POST.get('assignees' or None)
            for assign in assignees_members:
                assignee.assignees.add(assign)
            milestone = form4.save(commit=False)
            milestone.issue = issue
            milestone.save()
            return redirect('base:project_detail', id=id)

        elif form1.is_valid() and form2.is_valid() and form3.is_valid():
            issue = form1.save(commit=False)
            issue.project = project
            issue.created_by_user = request.user
            issue.updated_by_user = request.user
            issue.save()
            attachment = form2.save(commit=False)
            attachment.issue = issue
            attachment.updated_by_user = request.user
            attachment.save()
            assignee = form3.save(commit=False)
            assignee.issue = issue
            assignee.save()
            assignees_members = request.POST.get('assignees' or None)
            for assign in assignees_members:
                assignee.assignees.add(assign)
            return redirect('base:project_detail', id=id)

        elif form1.is_valid() and form2.is_valid():
            issue = form1.save(commit=False)
            issue.project=project
            issue.created_by_user = request.user
            issue.updated_by_user = request.user
            issue.save()
            attachment = form2.save(commit=False)
            attachment.issue = issue
            attachment.updated_by_user = request.user
            attachment.save()
            return redirect('base:project_detail', id = id)
        elif form1.is_valid():
            issue = form1.save(commit=False)
            issue.project=project
            issue.created_by_user = request.user
            issue.updated_by_user = request.user
            issue.save()
            return redirect('base:project_detail', id = id)

    return render(request,'projects/create_issue_template.html',context)