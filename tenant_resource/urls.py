from django.conf.urls import include, url
from tenant_resource.views import staff_views, client_views


urlpatterns = (
    url(r'^resource/info/(.*)/$', client_views.info_details_page, name='tenant_resource_details_info'),
    url(r'^resource/edit/(.*)/$', client_views.edit_details_page, name='tenant_resource_details_edit'),
    url(r'^resource/(.*)/new/$', client_views.create_page, name='tenant_resource_create'),
    url(r'^resource/(.*)/$', client_views.master_page, name='tenant_resource_master'),


    # STAFF
    url(r'^staff/resource/category/(.*)/info/(.*)/$', staff_views.staff_resource_details_info_page, name='tenant_resource_staff_resource_info_details'),
    url(r'^staff/resource/category/(.*)/edit/(.*)/$', staff_views.staff_resource_details_edit_page, name='tenant_resource_staff_resource_edit_details'),
    url(r'^staff/resource/category/(.*)/$', staff_views.staff_category_details_page, name='tenant_resource_staff_details'),
    url(r'^staff/resource/category$', staff_views.staff_category_master_page, name='tenant_resource_staff_category_master'),
    url(r'^staff/resource/create$', staff_views.staff_resource_create_page, name='tenant_resource_staff_resource_create'),
    url(r'^staff/resource/launchpad$', staff_views.staff_launchpad_page, name='tenant_resource_staff_launchpad_master'),

    # ENTREPRENEUR
    # url(r'^client/resource/category/(.*)/item/(.*)/$', staff_views.staff_resource_details_page, name='tenant_resource_staff_resource_details'),
    url(r'^client/resource/category$', client_views.client_category_master_page, name='tenant_resource_client_category_master'),
)
