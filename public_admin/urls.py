from django.conf.urls import include, url
from public_admin.views import dashboard_view, organization_view


urlpatterns = (
    url(r'^janitor/organization/create/(.*)/2/$', organization_view.organization_create_2_page, name='public_admin_organization_create_2'),
    url(r'^janitor/organization/create/(.*)/1/$', organization_view.organization_create_1_page, name='public_admin_organization_create_1'),
    url(r'^janitor/organization/initialize$', organization_view.organization_initialization_page, name='public_admin_organization_initialization'),
    url(r'^janitor/organization/list$', organization_view.organization_master_page, name='public_admin_organization_master'),
    url(r'^janitor/organization$', organization_view.organization_menu_page, name='public_admin_organization'),
    url(r'^janitor$', dashboard_view.dashboard_master_page, name='public_admin_dashboard_master'),
)
