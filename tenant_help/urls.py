from django.conf.urls import include, url
from tenant_help import views


urlpatterns = (
    url(r'^help$', views.master_page, name='tenant_help_master'),
)
