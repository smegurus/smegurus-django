from django.conf.urls import include, url
from tenant_workspace.views import workspace_view, module_view


urlpatterns = (
    # EXERCISE
    # url(r'^workspace/(.*)/module/(.*)/exercise/(.*)/$', exercise_view.master_page, name='tenant_workspace_exercise_master'),

    # MODULE
    url(r'^workspace/(.*)/module/(.*)/slide/(.*)/$', module_view.detail_page, name='tenant_workspace_module_detail'),
    url(r'^workspace/(.*)/module/(.*)/finish$', module_view.finish_master_page, name='tenant_workspace_module_finish_master'),
    url(r'^workspace/(.*)/module/(.*)/start$', module_view.start_master_page, name='tenant_workspace_module_start_master'),

    # WORKSPACE
    url(r'^workspace/create$', workspace_view.create_page, name='tenant_workspace_create'),
    url(r'^workspace/(.*)/$', workspace_view.master_page, name='tenant_workspace_master'),
)
