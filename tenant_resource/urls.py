from django.conf.urls import include, url
from tenant_resource import views


urlpatterns = (
    url(r'^resource/info/(.*)/$', views.resource_info_details_page, name='tenant_resource_details_info'),
    url(r'^resource/edit/(.*)/$', views.resource_edit_details_page, name='tenant_resource_details_edit'),
    url(r'^resource/new/$', views.resource_create_page, name='tenant_resource_create'),
    url(r'^resource/(.*)/$', views.resource_master_page, name='tenant_resource_master'),
    url(r'^resource-category$', views.resource_category_master_page, name='tenant_resource_category_master'),
)
