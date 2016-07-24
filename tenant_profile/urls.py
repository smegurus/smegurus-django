from django.conf.urls import patterns, include, url
from tenant_profile import views


urlpatterns = (
    url(r'^profile$', views.profile_page, name='tenant_profile'),
    url(r'^profile_settings$', views.profile_settings_page, name='tenant_profile_setting'),
    url(r'^locked$', views.locked_page, name='tenant_profile_lock'),
    url(r'^is_locked$', views.tenant_profile_is_locked_page, name='tenant_profile_is_locked'),

)
