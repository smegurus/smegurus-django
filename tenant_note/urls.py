from django.conf.urls import patterns, include, url
from tenant_note import views


urlpatterns = (
    url(r'^client/(.*)/note/$', views.master_page, name='tenant_note_master'),
    url(r'^client/(.*)/note/(.*)/$', views.details_page, name='tenant_note_details'),
)
