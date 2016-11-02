from django.conf.urls import include, url
from tenant_workspace import views


urlpatterns = (
    url(r'^workspace/create$', views.create_page, name='tenant_workspace_create'),
    url(r'^workspace/(.*)/$', views.modules_master_page, name='tenant_workspace_master'),
)
