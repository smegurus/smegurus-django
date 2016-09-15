from django.conf.urls import patterns, include, url
from public_admin.views import dashboard_view, organization_view


urlpatterns = (
    url(r'^janitor/organization/create/1/$', organization_view.organization_create_1_page, name='public_admin_organization_create_1'),
    url(r'^janitor/organization/list$', organization_view.organization_master_page, name='public_admin_organization_master'),
    url(r'^janitor/organization$', organization_view.organization_menu_page, name='public_admin_organization'),
    url(r'^janitor$', dashboard_view.dashboard_master_page, name='public_admin_dashboard_master'),
)
