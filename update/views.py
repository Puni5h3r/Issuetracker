from django.shortcuts import render,get_object_or_404,redirect

from .forms import IssueCloseForm, IssueCommentForm, IssueLikeForm
from base.models import Issue,Project, IssueComment, IssueLike


def update_issue(request,id):
    template_name = 'draft_detail.html'
    issue = get_object_or_404(Issue,pk=id)
    form = IssueCloseForm(instance=issue)
    comment = IssueComment.objects.filter(issue=issue)
    form2 = IssueCommentForm
    project = Project.objects.get(pk = issue.project.project_id)
    try:
        like_instance = IssueLike.objects.get(issue = issue)
        form3 = IssueLikeForm(instance=like_instance)
    except IssueLike.DoesNotExist:
        form3 = IssueLikeForm
        like_instance = None

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
                obj, created = IssueLike.objects.update_or_create(
                    issue=issue, action_by=request.user,
                    defaults={'like': issue_like.like, 'dislike':issue_like.dislike},
                )
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
                obj, created = IssueLike.objects.update_or_create(
                    issue=issue, action_by=request.user,
                    defaults={'like': issue_like.like, 'dislike': issue_like.dislike},
                )
            return redirect('update:update_issue', id = issue.id )

    context = {'form': form,
               'form2':form2,
               'comment':comment,
               'form3':form3,
               'project':project}
    return render(request,template_name,context)