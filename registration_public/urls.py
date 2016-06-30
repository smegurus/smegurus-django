from django.conf.urls import patterns, include, url
from registration_public import views


urlpatterns = (
    url(r'^register$', views.public_registration_page, name='public_registration'),
    url(r'^activation_required$', views.public_activation_required_page, name='public_activation_required'),
    url(r'^activate/(.*)/$', views.public_activate_page, name='public_activation'),
)
