from django.conf.urls import patterns, include, url
from tenant_resource import views


urlpatterns = (
    url(r'^resource$', views.resource_page, name='tenant_resource'),
)
