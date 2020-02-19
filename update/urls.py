from . import views
from django.urls import path


app_name = 'update'
urlpatterns = [
    path("projects/<uuid:id>/issue/update/", views.update_issue, name ='update_issue'),
    path("projects/<uuid:id>/project/update/", views.update_project, name ='update_project'),
    path("projects/<uuid:id>/issue/assignee/update/", views.create_add_assignee, name ='assignee_update'),
    path("projects/<uuid:id>/issue/color/update/", views.create_label, name ='label_update'),
]