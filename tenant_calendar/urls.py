from django.conf.urls import patterns, include, url
from tenant_calendar import views


urlpatterns = (
    url(r'^calendar$', views.calendar_page, name='tenant_calendar'),
)
