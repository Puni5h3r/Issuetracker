from . import views
from django.urls import path



app_name = 'base'
urlpatterns = [
    path("projects/", views.ProjectList.as_view(), name ='Project'),
    path("projects/create/", views.new_project, name ='create_project'),
    path("projects/<uuid:id>/issue/create/", views.create_issue, name ='create_issue'),
    path("projects/<uuid:id>/detail/", views.project_detail, name ='project_detail'),
    path("projects/<uuid:id>/issue/miletone/create", views.create_milestone, name ='milestone_create'),
]