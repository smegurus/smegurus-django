from django.conf.urls import patterns, include, url
from tenant_note import views


urlpatterns = (
    url(r'^client/(.*)/note/$', views.entrepreneur_master_page, name='tenant_note_entrepreneur_master'),
    url(r'^client/(.*)/note/(.*)/$', views.entrepreneur_details_page, name='tenant_note_entrepreneur_details'),
    url(r'^client/(.*)/note/create$', views.entrepreneur_create_page, name='tenant_note_entrepreneur_create'),
)
