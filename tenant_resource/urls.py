from django.conf.urls import patterns, include, url
from tenant_resource import views


urlpatterns = (
    url(r'^resource/info/(.*)/$', views.resource_info_details_page, name='tenant_resource_details_info'),
    url(r'^resource/edit/(.*)/$', views.resource_edit_details_page, name='tenant_resource_details_edit'),
    url(r'^resource/new/$', views.resource_create_page, name='tenant_resource_create'),
    url(r'^resource$', views.resource_page, name='tenant_resource_master'),
)
