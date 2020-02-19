from django.shortcuts import render,get_object_or_404,redirect

from .forms import IssueCloseForm, IssueCommentForm, IssueLikeForm, AddAssigneeForm, LabelFrom
from base.models import Issue,Project, IssueComment, IssueLike, Milestone, Assignees
from base.forms import CreateProject,ProjectAttachment
from django.template.context_processors import csrf

def update_issue(request,id):
    template_name = 'draft_detail.html'
    issue = get_object_or_404(Issue,pk=id)
    form = IssueCloseForm(instance=issue)
    comment = IssueComment.objects.filter(issue=issue)
    form2 = IssueCommentForm
    project = Project.objects.get(pk = issue.project.project_id)
    total_likes = IssueLike.objects.filter(issue=issue, like = True).count()
    total_dislikes = IssueLike.objects.filter(issue=issue, dislike=True).count()
    try:
        like_instance = IssueLike.objects.get(issue = issue, action_by = request.user)
        form3 = IssueLikeForm(instance=like_instance)
    except IssueLike.DoesNotExist:
        form3 = IssueLikeForm
        like_instance = None
    context = {'form': form,
               'form2': form2,
               'comment': comment,
               'form3': form3,
               'project': project,
               'issue':issue,
               'total_likes':total_likes,
               'total_dislikes':total_dislikes}
    try:
        milestone = Milestone.objects.filter(issue=issue)
        context['milestone'] = milestone
    except Milestone.DoesNotExist:
        context ['milestone'] = None
    try:
        assignee = Assignees.objects.get(issue=issue)
        context['assignee'] = assignee.assignees.all()
    except Assignees.DoesNotExist:
        context ['assignee'] = None

    if request.method == "POST":
        form = IssueCloseForm(request.POST, instance=issue)
        form2 = IssueCommentForm(request.POST or None)
        form3 = IssueLikeForm(request.POST or None)
        if form2.is_valid() and form.is_valid() and form3.is_valid():
            comment = form2.save(commit=False)
            comment.user = request.user
            comment.issue = issue
            comment.save()
            post = form.save(commit=False)
            post.updated_by_user = request.user
            post.save()
            if like_instance is None:
                issue_like = form3.save(commit=False)
                issue_like.issue = issue
                issue_like.action_by = request.user
                issue_like.save()
            else:
                issue_like = form3.save(commit=False)
                like_instance.like = issue_like.like
                like_instance.dislike = issue_like.dislike
                like_instance.save()
            return redirect('update:update_issue', id=issue.id)
        elif form.is_valid() :
            post = form.save(commit=False)
            post.updated_by_user = request.user
            post.save()
            if like_instance is None:
                issue_like = form3.save(commit=False)
                issue_like.issue = issue
                issue_like.action_by = request.user
                issue_like.save()
            else:
                issue_like = form3.save(commit=False)
                like_instance.like = issue_like.like
                like_instance.dislike = issue_like.dislike
                like_instance.save()
            return redirect('update:update_issue', id = issue.id )

    return render(request,template_name,context)



def update_project(request,id):
    project_instance = get_object_or_404(Project, project_id=id)
    project_form = CreateProject(instance=project_instance)
    attachment_form = ProjectAttachment
    context = {}
    context.update(csrf(request))
    context ['project_form'] = project_form
    context ['attachment_form'] = attachment_form

    if request.method == 'POST':
        form1 = CreateProject(request.POST or None)
        form2 = attachment_form(request.POST or None)
        if form1.is_valid() and form2.is_valid():
            update_project = form1.save(commit=False)
            project_instance.name = update_project.name
            project_instance.description = update_project.description
            project_instance.repository = update_project.repository
            members = request.POST.get('members' or None)
            project_instance.updated_by_user = request.user
            project_instance.save()
            project_instance.members.add(members)
            attachment = form2.save(commit=False)
            attachment.project = project_instance
            attachment.save()
            return redirect('base:Project')

        elif form1.is_valid():
            update_project = form1.save(commit=False)
            project_instance.name = update_project.name
            project_instance.description = update_project.description
            project_instance.repository = update_project.repository
            members = request.POST.get('members' or None)
            project_instance.updated_by_user = request.user
            project_instance.save()
            project_instance.members.add(members)
            return redirect('base:Project')

    return render(request, 'projects/create_project_template.html', context)



def create_add_assignee(request,id):
    assignee_form = AddAssigneeForm
    issue = get_object_or_404(Issue,pk=id)
    try:
        instance = Assignees.objects.get(issue=issue)
    except Assignees.DoesNotExist:
        instance = None
    context = {}
    context ['assignee_form'] = assignee_form
    context ['issue'] = issue
    if request.method == 'POST':
        assignee_form = assignee_form(request.POST)
        if assignee_form.is_valid():
            if instance is not None:
                members = request.POST.get('assignees' or None)
                instance.assignees.add(members)
            else:
                assignee = assignee_form.save(commit=False)
                assignee.issue = issue
                assignee.save()
                members = request.POST.get('assignees' or None)
                assignee.assignees.add(members)
        return redirect('update:update_issue', id=id)
    else:
        return render(request,'issues/add_assignnee.html',context)


def create_label(request,id):
    label_form = LabelFrom
    issue = get_object_or_404(Issue, pk = id)
    template_name = 'issues/color_picker.html'
    context = {}
    context ['label_form']=label_form
    context ['issue']=issue
    return render(request, template_name, context)
