from django.conf.urls import patterns, include, url
from authentication_public import views


urlpatterns = (
    url(r'^register$', views.public_registration_page, name='public_registration'),
    url(r'^activation_required$', views.public_activation_required_page, name='public_activation_required'),
    url(r'^activate/(.*)/$', views.public_activate_page, name='public_activation'),
    url(r'^login$', views.public_login_page, name='public_login'),
    url(r'^launchpad$', views.public_launchpad_page, name='public_launchpad'),
    url(r'^org_register$', views.public_org_registration_page, name='public_org_registration'),
)
