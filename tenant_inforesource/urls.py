from django.conf.urls import patterns, include, url
from tenant_inforesource import views


urlpatterns = (
    url(r'^resource$', views.resource_master_page, name='tenant_inforesource_master'),
)
