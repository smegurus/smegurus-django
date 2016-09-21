from django.conf.urls import patterns, include, url
from tenant_calendar import views


urlpatterns = (
    url(r'^calendar/new/$', views.calendar_create_page, name='tenant_calendar_create'),
    url(r'^calendar/(.*)/$', views.calendar_details_page, name='tenant_calendar_details'),
    url(r'^calendar$', views.calendar_master_page, name='tenant_calendar_master'),
)
