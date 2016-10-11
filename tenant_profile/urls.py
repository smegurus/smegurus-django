from django.conf.urls import include, url
from tenant_profile import views


urlpatterns = (
    url(r'^profile$', views.profile_page, name='tenant_profile'),
    url(r'^settings/profile$', views.profile_settings_profile_page, name='tenant_profile_setting_profile'),
    url(r'^settings/address$', views.profile_settings_address_page, name='tenant_profile_setting_address'),
    url(r'^settings/password$', views.profile_settings_password_page, name='tenant_profile_setting_password'),
    url(r'^settings/notification$', views.profile_settings_notification_page, name='tenant_profile_setting_notification'),
    url(r'^locked$', views.locked_page, name='tenant_profile_lock'),
    url(r'^is_locked$', views.tenant_profile_is_locked_page, name='tenant_profile_is_locked'),
)
