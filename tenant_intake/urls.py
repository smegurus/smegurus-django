from django.conf.urls import patterns, include, url
from tenant_intake import views


urlpatterns = (
    # DECORATORS
    url(r'^intake/check$', views.check_page, name='tenant_intake_check'),
    url(r'^intake/has_completed$', views.has_completed_intake_page, name='tenant_intake_has_completed'),

    # Entrepreneur
    url(r'^intake/entrepreneur/step/1$', views.intake_entr_step_one_page, name='tenant_intake_entr_step_one'),
    url(r'^intake/entrepreneur/step/2$', views.intake_entr_step_two_page, name='tenant_intake_entr_step_two'),
    url(r'^intake/entrepreneur/step/3$', views.intake_entr_step_three_page, name='tenant_intake_entr_step_three'),
    url(r'^intake/entrepreneur/step/4$', views.intake_entr_step_four_page, name='tenant_intake_entr_step_four'),
    url(r'^intake/entrepreneur/step/5$', views.intake_entr_step_five_page, name='tenant_intake_entr_step_five'),
    url(r'^intake/entrepreneur/step/6$', views.intake_entr_step_six_page, name='tenant_intake_entr_step_six'),
)