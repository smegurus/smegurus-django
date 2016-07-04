from django.conf.urls import patterns, include, url
from authentication_public import views


urlpatterns = (
    url(r'^register$', views.public_user_registration_page, name='public_user_registration'),
    url(r'^activation_required$', views.public_user_activation_required_page, name='public_user_activation_required'),
    url(r'^activate/(.*)/$', views.public_user_activate_page, name='public_user_activation'),
    url(r'^login$', views.public_user_login_page, name='public_user_login'),
    url(r'^launchpad$', views.public_user_launchpad_page, name='public_user_launchpad'),
    url(r'^org_register$', views.public_org_registration_page, name='public_org_registration'),
    url(r'^org_successful_register$', views.public_org_successful_registration, name='public_org_successful_registration'),
)
