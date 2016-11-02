from django.conf.urls import include, url
from tenant_workspace.views import workspace_view, module_view


urlpatterns = (
    # MODULE
    url(r'^workspace/(.*)/module/(.*)/slide/(.*)/$', module_view.detail_page, name='tenant_workspace_module_detail'),
    url(r'^workspace/(.*)/module/(.*)/$', module_view.master_page, name='tenant_workspace_module_master'),

    # WORKSPACE
    url(r'^workspace/create$', workspace_view.create_page, name='tenant_workspace_create'),
    url(r'^workspace/(.*)/$', workspace_view.master_page, name='tenant_workspace_master'),
)
