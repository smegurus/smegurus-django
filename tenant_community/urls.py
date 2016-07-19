from django.conf.urls import patterns, include, url
from tenant_community import views


urlpatterns = (
    url(r'^community$', views.community_page, name='tenant_community'),
)
