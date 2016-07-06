from django.conf.urls import patterns, include, url
from foundation_auth import views


urlpatterns = (
    url(r'^register$', views.user_registration_page, name='foundation_auth_user_registration'),
    url(r'^activation_required$', views.user_activation_required_page, name='foundation_auth_user_activation_required'),
    url(r'^activate/(.*)/$', views.user_activate_page, name='foundation_auth_user_activation'),
    url(r'^login$', views.user_login_page, name='foundation_auth_user_login'),
    url(r'^launchpad$', views.user_launchpad_page, name='foundation_auth_user_launchpad'),
    url(r'^register/organization$', views.organization_registration_page, name='foundation_auth_org_registration'),
    url(r'^register/organization/success$', views.organization_successful_registration, name='foundation_auth_org_successful_registration'),
)