from django.conf.urls import patterns, include, url
from tenant_task import views


urlpatterns = (
    url(r'^task/(.*)/$', views.task_details_page, name='tenant_task_details'),
    url(r'^task$', views.task_master_page, name='tenant_task_master'),
)
