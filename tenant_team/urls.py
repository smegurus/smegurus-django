from django.conf.urls import patterns, include, url
from tenant_team import views


urlpatterns = (
    url(r'^team$', views.master_page, name='tenant_team_master'),
)
