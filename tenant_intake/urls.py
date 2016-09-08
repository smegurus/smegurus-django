from django.conf.urls import patterns, include, url
from tenant_intake.views import entrepreneur_view, employee_view, decorator_view


urlpatterns = (
    # Decorators
    url(r'^intake/check$', decorator_view.check_page, name='tenant_intake_check'),
    url(r'^intake/has_completed$', decorator_view.has_completed_intake_page, name='tenant_intake_has_completed'),

    # Entrepreneur - Round One
    url(r'^intake/entrepreneur/round_1/step/1$', entrepreneur_view.intake_entr_round_one_step_one_page, name='tenant_intake_entr_round_one_step_one'),
    url(r'^intake/entrepreneur/round_1/step/2$', entrepreneur_view.intake_entr_round_one_step_two_page, name='tenant_intake_entr_round_one_step_two'),
    url(r'^intake/entrepreneur/round_1/step/3$', entrepreneur_view.intake_entr_round_one_step_three_page, name='tenant_intake_entr_round_one_step_three'),
    url(r'^intake/entrepreneur/round_1/step/4$', entrepreneur_view.intake_entr_round_one_step_four_page, name='tenant_intake_entr_round_one_step_four'),
    url(r'^intake/entrepreneur/round_1/step/5$', entrepreneur_view.intake_entr_round_one_step_five_page, name='tenant_intake_entr_round_one_step_five'),

    # Entrepreneur - Round Two
    url(r'^intake/entrepreneur/round_2/step/1$', entrepreneur_view.intake_entr_round_two_step_one_page, name='tenant_intake_entr_step_one'),


    # TODO: Implement.
    url(r'^intake/entrepreneur/finished$', entrepreneur_view.intake_round_one_finished_page, name='tenant_intake_finished'),

    # Employee
    url(r'^intake$', employee_view.intake_master_page, name='tenant_intake_employee_master'),
    url(r'^intake/(.*)/$', employee_view.intake_details_page, name='tenant_intake_employee_details'),
)
