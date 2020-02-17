from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

import uuid

User = get_user_model()

# a uuid will be generated which will be used as the primary key when making models

# class IdMixin(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#
#     class Meta:
#         abstract = True

#store information about when the updated was done and by which user

# class UpdatedByMixin(models.Model):
#     updated_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='updated_by')
#     updatd_time = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         abstract = True

#store information about the creation when the fields were created

# class CreatedOnMixin(models.Model):
#     created_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_by')
#     created_on = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         abstract = True

#an abstract base model, which store information about attachment like images, files.

# class AttachmentMixin(models.Model):
#     image = models.ImageField()
#     files = models.FileField()
#
#     class Meta:
#         abstract = True


#A user can have many projects, which is created by him,
#A project can have many members, who are the users themselves
# a user can be involved in many projects
# the class inherits base models IdMixin, UpdatedByMixin, CreatedOnMixin
#for the time being the repository is an url reference - a reference where repositort exists

class Project(models.Model):
    project_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    updated_by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by',blank=True, editable=True)
    updated_time = models.DateTimeField(auto_now=True)
    created_by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by', editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=256)
    repository = models.URLField()
    members = models.ManyToManyField(User, related_name='project_members', default=True)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name +" "+ self.description

# Every project can have an attachment involved, could be an image/ pdf.

class ProjectAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_attachment')
    image = models.ImageField(blank=True)
    files = models.FileField(blank=True)



# every project must have Position, where we can keep information about the privileges a user has
# - the permission to post or retrieve object
# class Position(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     user_members = models.ForeignKey(User, on_delete=models.CASCADE, related_name='position_of_user')
#     admin_priviledge = models.BooleanField(default=True)


#An issue can be raised within a project where members will
#see the title of the issue raised, issues can have Description
#can have an attached file/photo, a issue can be open or closed
#issues can be confidential which can be only seen by selected
#members of the team.
#Issues have a due date.
#Isseus can have a milestrone, comments, label and assignees.


class Issue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    updated_by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_updated_by', blank=True)
    updatd_time = models.DateTimeField(auto_now_add=True)
    created_by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_created_by')
    created_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null = True)
    open = models.BooleanField(default=True)
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank= True)
    restrict_access = models.BooleanField(default=False)
    project = models.ForeignKey(Project,on_delete=models.CASCADE, related_name='project_issue')
    weight = models.IntegerField(validators=[MinValueValidator(0)], blank=True, default= None, null= True)




# #assignees can be tracked to the user,
# #assigness can be restricted
#
class Assignees(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='assignee_issues')
    assignees = models.ManyToManyField(User, related_name='assignees',blank=True)
    access = models.BooleanField(default=True)


class IssueAttachment(models.Model):
    issue = models.ForeignKey(Issue,on_delete=models.CASCADE, related_name= 'issue_attachment')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    updated_by_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='attachment_updated_by')
    updatd_time = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True)
    files = models.FileField(blank=True)


 #issues can have milestone
class Milestone(models.Model):
     title = models.CharField(max_length=256)
     description = models.TextField(blank=True, null=True)
     start_date = models.DateField(blank=True, null=True)
     Due_date = models.DateField(blank=True, null=True)
     issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='issue_milestones')



# #milestone can have attachment
class MilestoneAttachment(models.Model):
    milestone = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='milestone_attachment')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    updated_by_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='milestone_updated_by')
    updatd_time = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True)
    files = models.FileField(blank=True)




# #issues can have comment
class IssueComment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='issue_comment')
    comment = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name= 'commented_by_user')
    created_on = models.DateTimeField(auto_now_add=True)

class IssueLike(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name= 'issue_like')
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    action_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='like_dislike_by_user')

# #issues can have labels
# class Label(IdMixin):
#     issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='issue_label')
#     color = models.IntegerField()
#     priority = models.BooleanField(default=False)
#
# #issues can have weights

