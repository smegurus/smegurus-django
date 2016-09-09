from django.conf.urls import patterns, include, url
from tenant_intake.views import entrepreneur_view, employee_view, decorator_view


urlpatterns = (
    # Decorators
    url(r'^intake/check$', decorator_view.check_page, name='tenant_intake_check'),
    url(r'^intake/has_completed$', decorator_view.has_completed_intake_page, name='tenant_intake_has_completed'),

    # Entrepreneur - Round One Intake
    url(r'^intake/entrepreneur/step-1-1$', entrepreneur_view.intake_entr_round_one_step_one_page, name='tenant_intake_entr_round_one_step_one'),
    url(r'^intake/entrepreneur/step-1-2$', entrepreneur_view.intake_entr_round_one_step_two_page, name='tenant_intake_entr_round_one_step_two'),
    url(r'^intake/entrepreneur/step-1-3$', entrepreneur_view.intake_entr_round_one_step_three_page, name='tenant_intake_entr_round_one_step_three'),
    url(r'^intake/entrepreneur/step-1-4$', entrepreneur_view.intake_entr_round_one_step_four_page, name='tenant_intake_entr_round_one_step_four'),
    url(r'^intake/entrepreneur/step-1-5$', entrepreneur_view.intake_entr_round_one_step_five_page, name='tenant_intake_entr_round_one_step_five'),

    # Entrepreneur - Round Two Intake
    url(r'^intake/entrepreneur/step-2-1$', entrepreneur_view.intake_entr_round_two_step_one_page, name='tenant_intake_entr_round_two_step_one'),
    url(r'^intake/entrepreneur/step-2-2$', entrepreneur_view.intake_entr_round_two_step_two_page, name='tenant_intake_entr_round_two_step_two'),
    url(r'^intake/entrepreneur/step-2-3$', entrepreneur_view.intake_entr_round_two_step_three_page, name='tenant_intake_entr_round_two_step_three'),
    url(r'^intake/entrepreneur/step-2-4$', entrepreneur_view.intake_entr_round_two_step_four_page, name='tenant_intake_entr_round_two_step_four'),
    url(r'^intake/entrepreneur/step-2-5$', entrepreneur_view.intake_entr_round_two_step_five_page, name='tenant_intake_entr_round_two_step_five'),

    # Entrepreneur - Finished Intake
    url(r'^intake/entrepreneur/finished$', entrepreneur_view.intake_round_two_finished_page, name='tenant_intake_finished'),

    # Employee - Intake Review
    url(r'^intake$', employee_view.intake_master_page, name='tenant_intake_employee_master'),
    url(r'^intake/(.*)/$', employee_view.intake_details_page, name='tenant_intake_employee_details'),
)
