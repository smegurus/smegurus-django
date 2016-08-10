from django.conf.urls import patterns, include, url
from tenant_help import views


urlpatterns = (
    url(r'^help$', views.master_page, name='tenant_help_master'),
)
