from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.list import ListView
from django.db.models import Q
from django.template.context_processors import csrf
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


from .forms import CreateProject, ProjectAttachmentForm, IssueForm, IssueAttachmentForm, IssueAssigneeForm, MilestoneForm
from .models import Project, Issue, ProjectAttachment


@method_decorator(login_required, name='dispatch')
class ProjectList(ListView):
    template_name = 'projects/project_index.html'
    paginate_by = 100

    def get_queryset(self):
        return Project.objects.filter(Q(created_by_user= self.request.user) | Q(members= self.request.user)).order_by('created_on').distinct()


@login_required
def new_project(request):
    project_form = CreateProject
    attachment_form = ProjectAttachmentForm
    context = {}
    context.update(csrf(request))
    context ['project_form'] = project_form(prefix='form1')
    context ['attachment_form'] = attachment_form(prefix='form2')

    if request.method == 'POST':
        form1 = project_form(request.POST, prefix='form1')
        form2 = attachment_form(request.POST, prefix='form2')
        if all([form1.is_valid(),form2.is_valid()]):
            project = form1.save(commit=False)
            members = request.POST.getlist('form1-members')
            project.created_by_user = request.user
            project.updated_by_user = request.user
            project.save()
            project.members.add(*members)
            attachment = form2.save(commit=False)
            attachment.project = project
            attachment.save()
            return redirect('base:Project')

        elif form1.is_valid():
            print('this is not enterted')
            project = form1.save(commit=False)
            project.created_by_user = request.user
            project.updated_by_user = request.user
            members = request.POST.getlist('form1-members')
            project.save()
            project.members.add(*members)
            return redirect('base:Project')

    return render(request, 'projects/create_project_template.html', context)





@login_required
def project_detail(request, id):
    project = Project.objects.get(pk = id)
    attachment = ProjectAttachment.objects.filter(project=project)
    issue = Issue.objects.filter(project__project_id=id).order_by('-created_on')
    open = len([x for x in issue if x.open == True])
    close = len([x for x in issue if x.open == False])
    context = {}
    context ['project'] = project
    context['issue'] = issue
    context ['open_total'] = open
    context ['close_total'] = close
    context ['attachment_list'] = attachment
    return render(request,'projects/project_detail.html',context)



@login_required
def create_issue(request, id):
    project = Project.objects.get(pk=id)
    form1 = IssueForm
    form2 = IssueAttachmentForm
    form3 = IssueAssigneeForm
    context = {}
    context.update(csrf(request))
    context['issue_form'] = form1(prefix='form1')
    context['attachment_form'] = form2(prefix='form2')
    context['assinee_form'] = form3(prefix='form3')
    context['project'] = project

    if request.method == 'POST':
        form1 = form1(request.POST, prefix='form1')
        form2 = form2(request.POST, prefix='form2')
        form3 = form3(request.POST, prefix='form3')

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
            assignees_members = request.POST.getlist('form3-assignees')
            assignee.assignees.add(*assignees_members)
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

        context['issue_form'] = form1
        context['attachment_form'] = form2
        context['assinee_form'] = form3

    return render(request,'projects/create_issue_template.html',context)



@login_required
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