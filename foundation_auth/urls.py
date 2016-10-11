from django.conf.urls import include, url
from foundation_auth import views


urlpatterns = (
    url(r'^register$', views.user_registration_page, name='foundation_auth_user_registration'),
    url(r'^activation_required$', views.user_activation_required_page, name='foundation_auth_user_activation_required'),
    url(r'^activate/(.*)/$', views.user_activate_page, name='foundation_auth_user_activation'),
    url(r'^login$', views.user_login_page, name='foundation_auth_user_login'),
    url(r'^launchpad$', views.user_launchpad_page, name='foundation_auth_user_launchpad'),
    url(r'^register/organization$', views.organization_registration_page, name='foundation_auth_org_registration'),
    url(r'^register/success$', views.organization_successful_registration_page, name='foundation_auth_org_successful_registration'),
    url(r'^password_reset$', views.password_reset_page, name='foundation_auth_password_reset'),
    url(r'^password_reset_sent$', views.password_reset_sent_page, name='foundation_auth_password_reset_sent'),
    url(r'^password_reset/(.*)/$', views.password_change_page, name='foundation_auth_password_reset_and_change'),
)
