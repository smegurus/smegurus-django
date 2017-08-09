from django.conf.urls import include, url
from tenant_profile.views import me_views, org_views


urlpatterns = (
    # Me Views
    url(r'^profile$', me_views.profile_page, name='tenant_profile'),
    url(r'^settings/profile$', me_views.profile_settings_profile_page, name='tenant_profile_setting_profile'),
    url(r'^settings/address$', me_views.profile_settings_address_page, name='tenant_profile_setting_address'),
    url(r'^settings/password$', me_views.profile_settings_password_page, name='tenant_profile_setting_password'),
    url(r'^settings/notification$', me_views.profile_settings_notification_page, name='tenant_profile_setting_notification'),
    url(r'^locked$', me_views.locked_page, name='tenant_profile_lock'),
    url(r'^is_locked$', me_views.tenant_profile_is_locked_page, name='tenant_profile_is_locked'),

    # Organization Views
    url(r'^settings/organization/profile$', org_views.profile_settings_profile_page, name='tenant_profile_setting_organization_profile'),
    url(r'^settings/organization/address$', org_views.profile_settings_address_page, name='tenant_profile_setting_organization_address'),
    url(r'^settings/organization/preferences$', org_views.profile_settings_preferences_page, name='tenant_profile_setting_organization_preferences'),
    url(r'^settings/organization/program_tags$', org_views.profile_settings_program_tags_page, name='tenant_profile_setting_organization_program_tags'),
    url(r'^settings/organization/client_tags$', org_views.profile_settings_client_tags_page, name='tenant_profile_setting_organization_client_tags'),
    url(r'^settings/organization/perks$', org_views.profile_settings_perks_page, name='tenant_profile_setting_organization_perks'),
    url(r'^settings/organization/affiliate_links$', org_views.profile_settings_affiliate_links_page, name='tenant_profile_setting_organization_affiliate_links'),

)
