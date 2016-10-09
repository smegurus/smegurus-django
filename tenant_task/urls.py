from django.conf.urls import patterns, include, url
from tenant_task import views


urlpatterns = (
    url(r'^task/edit/(.*)/$', views.task_details_page, name='tenant_task_details'),
    url(r'^task/new/$', views.task_master_create_page, name='tenant_task_master_create'),
    url(r'^task-open$', views.task_open_master_page, name='tenant_task_master_open'),
    url(r'^task-closed$', views.task_closed_master_page, name='tenant_task_master_closed'),
)
