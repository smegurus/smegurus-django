from django.conf.urls import include, url
from tenant_reception.views import dashboard_view, decorator_view, tasks_view, calendar_view, resource_view, message_view, workspace_view


urlpatterns = (
    # Decorator
    url(r'^reception/is_required$', decorator_view.is_required_page, name='tenant_reception_is_required'),

    # Workspace
    url(r'^reception/workspace/(.*)/(.*)/finish$', workspace_view.finish_master_page, name='tenant_reception_workspace_finish_master'),
    url(r'^reception/workspace/(.*)/start$', workspace_view.start_master_page, name='tenant_reception_workspace_start_master'),
    url(r'^reception/workspace/(.*)/(.*)/$', workspace_view.workspace_detail_page, name='tenant_reception_workspace_detail'),

    # Calendar
    url(r'^reception/calendar/(.*)/$', calendar_view.reception_calendar_details_page, name='tenant_reception_calendar_details'),
    url(r'^reception/calendar$', calendar_view.reception_calendar_master_page, name='tenant_reception_calendar_master'),

    # Task
    url(r'^reception/tasks/(.*)/$', tasks_view.task_details_page, name='tenant_reception_tasks_details'),
    url(r'^reception/tasks$', tasks_view.reception_tasks_master_page, name='tenant_reception_tasks_master'),

    # Resources
    url(r'^reception/resource/(.*)/(.*)/$', resource_view.resource_details_page, name='tenant_reception_resource_details'),
    url(r'^reception/resource/(.*)/$', resource_view.resource_master_page, name='tenant_reception_resource_master'),
    url(r'^reception/resource$', resource_view.category_master_page, name='tenant_reception_resource_category_master'),

    # Messenger
    url(r'^reception/conversation/(.*)/$', message_view.conversation_page, name='tenant_reception_message_detail'),
    url(r'^reception/composer$', message_view.compose_page, name='tenant_reception_message_create'),
    url(r'^reception/inbox$', message_view.inbox_page, name='tenant_reception_message_master'),

    # Dashboard
    url(r'^reception$', dashboard_view.reception_dashboard_master_page, name='tenant_reception'),
)
