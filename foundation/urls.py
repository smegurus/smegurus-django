from django.conf.urls import patterns, include, url
from foundation.views import decoratorsview


urlpatterns = (
    # url(r'^tenant/name$', views.tenant_name, name='tenant_name'),
    # url(r'^tenant/access$', views.tenant_access_status, name='tenant_access_status'),
    url(r'^tenant/is_valid$', decoratorsview.tenant_is_valid, name='tenant_is_valid'),
)
