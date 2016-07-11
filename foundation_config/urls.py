from django.conf.urls import patterns, include, url
from foundation_config import views


urlpatterns = (
    # Organization
    url(r'^config/organization/step/1$', views.config_org_step_one_page, name='foundation_auth_config_org_step_one'),
    url(r'^config/organization/step/2$', views.config_org_step_two_page, name='foundation_auth_config_org_step_two'),
    url(r'^config/organization/step/3$', views.config_org_step_three_page, name='foundation_auth_config_org_step_three'),
    url(r'^config/organization/step/4$', views.config_org_step_four_page, name='foundation_auth_config_org_step_four'),
    url(r'^config/organization/step/5$', views.config_org_step_five_page, name='foundation_auth_config_org_step_five'),
    url(r'^config/organization/step/6$', views.config_org_step_six_page, name='foundation_auth_config_org_step_six'),
    url(r'^config/organization/step/7$', views.config_org_step_seven_page, name='foundation_auth_config_org_step_seven'),
    url(r'^config/organization/step/8$', views.config_org_step_eight_page, name='foundation_auth_config_org_step_eight'),
    
    # Entrepreneur
    url(r'^config/entrepreneur/step/1$', views.config_entr_step_one_page, name='foundation_auth_config_entr_step_one'),
    url(r'^config/entrepreneur/step/2$', views.config_entr_step_two_page, name='foundation_auth_config_entr_step_two'),
    url(r'^config/entrepreneur/step/3$', views.config_entr_step_three_page, name='foundation_auth_config_entr_step_three'),
    url(r'^config/entrepreneur/step/4$', views.config_entr_step_four_page, name='foundation_auth_config_entr_step_four'),
)
