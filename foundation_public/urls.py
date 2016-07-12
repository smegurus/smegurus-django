from django.conf.urls import patterns, include, url
from foundation_public.views import decoratorsview


urlpatterns = (
    # url(r'^tenant/name$', views.tenant_name, name='tenant_name'),
    # url(r'^tenant/access$', views.tenant_access_status, name='tenant_access_status'),
    url(r'^tenant/is_valid$', decoratorsview.tenant_is_valid, name='tenant_is_valid'),
    url(r'^group/is_entrepreneur$', decoratorsview.group_is_entrepreneur, name='group_is_entrepreneur'),
    url(r'^group/is_org_admin$', decoratorsview.group_is_org_admin, name='group_is_org_admin'),
)
