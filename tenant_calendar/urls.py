from django.conf.urls import include, url
from tenant_calendar import views


urlpatterns = (
    url(r'^calendar/info/(.*)/$', views.calendar_info_details_page, name='tenant_calendar_details_info'),
    url(r'^calendar/edit/(.*)/$', views.calendar_edit_details_page, name='tenant_calendar_details_edit'),
    url(r'^calendar/new/$', views.calendar_create_page, name='tenant_calendar_create'),
    url(r'^calendar$', views.calendar_master_page, name='tenant_calendar_master'),
)
