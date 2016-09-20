from django.conf.urls import patterns, include, url
from tenant_reception.views import dashboard_view, decorator_view, tasks_view


urlpatterns = (
    url(r'^reception/tasks/(.*)/$', tasks_view.task_details_page, name='tenant_reception_tasks_details'),
    url(r'^reception/is_required$', decorator_view.is_required_page, name='tenant_reception_is_required'),
    url(r'^reception/tasks$', tasks_view.reception_tasks_master_page, name='tenant_reception_tasks_master'),
    url(r'^reception$', dashboard_view.reception_dashboard_master_page, name='tenant_reception'),
)
