from django.conf.urls import include, url
from tenant_task import views


urlpatterns = (
    url(r'^task/info/(.*)/$', views.task_info_details_page, name='tenant_task_details_info'),
    url(r'^task/edit/(.*)/$', views.task_edit_details_page, name='tenant_task_details_edit'),
    url(r'^task/new/$', views.task_master_create_page, name='tenant_task_master_create'),
    url(r'^task-open$', views.task_open_master_page, name='tenant_task_master_open'),
    url(r'^task-closed$', views.task_closed_master_page, name='tenant_task_master_closed'),
)
