from django.conf.urls import patterns, include, url
from registration_public import views


urlpatterns = (
    url(r'^register$', views.org_owner_registration_page, name='org_owner_registration'),
    url(r'^activation_required$', views.org_owner_activation_required_page, name='org_owner_activation_required'),
    # url(r'^registration/pre-intake$', views.registration_stage_2_page, name='registration_stage2'),
    # url(r'^registration/intake$', views.registration_stage_3_page, name='registration_stage3'),
)
