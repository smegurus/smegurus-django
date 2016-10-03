from django.conf.urls import patterns, include, url
from tenant_team import views


urlpatterns = (
    url(r'^team/update/(.*)/$', views.update_page, name='tenant_team_update'),
    url(r'^team/create$', views.create_page, name='tenant_team_create'),
    url(r'^team$', views.master_page, name='tenant_team_master'),
)
