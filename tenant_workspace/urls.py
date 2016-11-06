from django.conf.urls import include, url
from tenant_workspace.views import workspace_view, module_view, exercise_view


urlpatterns = (
    # EXERCISE
    url(r'^workspace/(.*)/exercise/(.*)/question/last/$', exercise_view.last_detail_page_redirect, name='tenant_workspace_exercise_last_detail_redirect'),
    url(r'^workspace/(.*)/exercise/(.*)/question/(.*)/$', exercise_view.detail_page, name='tenant_workspace_exercise_detail'),
    url(r'^workspace/(.*)/exercise/(.*)/$', exercise_view.master_page_redirect, name='tenant_workspace_exercise_master_redirect'),

    # MODULE
    url(r'^workspace/(.*)/module/(.*)/finish$', module_view.finish_master_page, name='tenant_workspace_module_finish_master'),
    url(r'^workspace/(.*)/module/(.*)/start$', module_view.start_master_page, name='tenant_workspace_module_start_master'),
    url(r'^workspace/(.*)/module/(.*)/(.*)/$', module_view.detail_page, name='tenant_workspace_module_detail'),

    # WORKSPACE
    url(r'^workspace/create$', workspace_view.create_page, name='tenant_workspace_create'),
    url(r'^workspace/(.*)/$', workspace_view.master_page, name='tenant_workspace_master'),
)
