from django.conf.urls import patterns, include, url
from tenant_task import views


urlpatterns = (
    url(r'^tasks$', views.tasks_list_page, name='tenant_task'),
    url(r'^tasks/intake$', views.intake_master_page, name='tenant_task_intake'),
    url(r'^tasks/intake/(.*)/$', views.intake_details_page, name='tenant_task_intake_details'),
)
