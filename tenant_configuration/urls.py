from django.conf.urls import include, url
from tenant_configuration.views import entrepreneur_view, organization_view


urlpatterns = (
    # Organization
    url(r'^config/organization/step/1$', organization_view.config_org_step_one_page, name='foundation_auth_config_org_step_one'),
    url(r'^config/organization/step/2$', organization_view.config_org_step_two_page, name='foundation_auth_config_org_step_two'),
    url(r'^config/organization/step/3$', organization_view.config_org_step_three_page, name='foundation_auth_config_org_step_three'),
    url(r'^config/organization/step/4$', organization_view.config_org_step_four_page, name='foundation_auth_config_org_step_four'),
    url(r'^config/organization/step/5$', organization_view.config_org_step_five_page, name='foundation_auth_config_org_step_five'),
    url(r'^config/organization/step/6$', organization_view.config_org_step_six_page, name='foundation_auth_config_org_step_six'),
    url(r'^config/organization/step/7$', organization_view.config_org_step_seven_page, name='foundation_auth_config_org_step_seven'),
    url(r'^config/organization/step/8$', organization_view.config_org_step_eight_page, name='foundation_auth_config_org_step_eight'),

    # Entrepreneur
    url(r'^config/entrepreneur/step/1$', entrepreneur_view.config_entr_step_one_page, name='foundation_auth_config_entr_step_one'),
    url(r'^config/entrepreneur/step/2$', entrepreneur_view.config_entr_step_two_page, name='foundation_auth_config_entr_step_two'),
    url(r'^config/entrepreneur/step/3$', entrepreneur_view.config_entr_step_three_page, name='foundation_auth_config_entr_step_three'),
    url(r'^config/entrepreneur/step/4$', entrepreneur_view.config_entr_step_four_page, name='foundation_auth_config_entr_step_four'),
    url(r'^config/entrepreneur/step/5$', entrepreneur_view.config_entr_step_five_page, name='foundation_auth_config_entr_step_five'),
    url(r'^config/entrepreneur/step/6$', entrepreneur_view.config_entr_step_six_page, name='foundation_auth_config_entr_step_six'),
    url(r'^config/entrepreneur/step/7$', entrepreneur_view.config_entr_step_seven_page, name='foundation_auth_config_entr_step_seven'),
    url(r'^config/entrepreneur/step/8$', entrepreneur_view.config_entr_step_eight_page, name='foundation_auth_config_entr_step_eight'),
    url(r'^config/entrepreneur/step/9$', entrepreneur_view.config_entr_step_nine_page, name='foundation_auth_config_entr_step_nine'),
    url(r'^config/entrepreneur/step/10$', entrepreneur_view.config_entr_step_ten_page, name='foundation_auth_config_entr_step_ten'),
)
