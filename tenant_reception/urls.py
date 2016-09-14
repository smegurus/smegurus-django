from django.conf.urls import patterns, include, url
from tenant_reception.views import reception_view


urlpatterns = (
    # url(r'^reception/has_completed$', decorator_view.has_completed_intake_page, name='tenant_intake_has_completed'),
    url(r'^reception$', reception_view.reception_master_page, name='tenant_reception'),
)
