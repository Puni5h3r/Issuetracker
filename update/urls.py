from . import views
from django.urls import path


app_name = 'update'
urlpatterns = [
    path("projects/<uuid:id>/issue/update/", views.update_issue, name ='update_issue'),
]