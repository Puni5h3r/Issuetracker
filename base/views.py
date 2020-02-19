from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.views import View
from django.views.generic.list import ListView
from django.db.models import Q
from django.template.context_processors import csrf
from django.shortcuts import redirect, reverse

from .forms import CreateProject, ProjectAttachment, IssueForm, IssueAttachmentForm, IssueAssigneeForm, MilestoneForm
from .models import Project, Issue, Assignees, Milestone


class ProjectList(ListView):
    template_name = 'projects/project_index.html'
    paginate_by = 100

    def get_queryset(self):
        return Project.objects.filter(Q(created_by_user= self.request.user) | Q(members= self.request.user)).order_by('created_on').distinct()


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
            project.members.add(members)
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
    issue = Issue.objects.filter(project__project_id=id).order_by('-created_on')
    open = len([x for x in issue if x.open == True])
    close = len([x for x in issue if x.open == False])
    context = {}
    context ['project'] = project
    context['issue'] = issue
    context ['open_total'] = open
    context ['close_total'] = close
    return render(request,'projects/project_detail.html',context)



def create_issue(request, id):
    project = Project.objects.get(pk=id)
    issue_form = IssueForm
    attachment_form = IssueAttachmentForm
    assignee_form = IssueAssigneeForm
    context = {}
    context.update(csrf(request))
    context ['issue_form'] = issue_form
    context ['attachment_form'] = attachment_form
    context ['assinee_form'] = IssueAssigneeForm
    context ['project'] = project

    if request.method == 'POST':
        form1 = issue_form(request.POST or None)
        form2 = attachment_form(request.POST or None)
        form3 = assignee_form(request.POST or None)

        if form1.is_valid() and form2.is_valid() and form3.is_valid():
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
            assignee.assignees.add(assignees_members)
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
            assignee.assignees.add(assignees_members)
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


def create_milestone(request,id):
    milestone_form = MilestoneForm
    issue = get_object_or_404(Issue,pk=id)
    context = {}
    context ['milestone_form'] = milestone_form
    context ['issue'] = issue
    if request.method == 'POST':
        milestone_form = milestone_form(request.POST)
        if milestone_form.is_valid():
            milestone = milestone_form.save(commit=False)
            milestone.issue = issue
            milestone.save()
            return redirect('update:update_issue', id=id)
    else:
        return render(request,'projects/milestone_create.html',context)