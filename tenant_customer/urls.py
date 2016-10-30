from django.conf.urls import include, url
from tenant_customer.views import entrepreneur_view


urlpatterns = (
    url(r'^client/entrepreneur/update/(.*)/$', entrepreneur_view.update_page, name='tenant_customer_entrepreneur_update'),
    url(r'^client/entrepreneur/(.*)/create/step-3$', entrepreneur_view.create_step_three_page, name='tenant_customer_entrepreneur_create_step_3'),
    url(r'^client/entrepreneur/(.*)/create/step-2$', entrepreneur_view.create_step_two_page, name='tenant_customer_entrepreneur_create_step_2'),
    url(r'^client/entrepreneur/(.*)/create/step-1$', entrepreneur_view.create_step_one_page, name='tenant_customer_entrepreneur_create_step_1'),
    url(r'^client/entrepreneur/create$', entrepreneur_view.create_page, name='tenant_customer_entrepreneur_create'),
    url(r'^client/entrepreneur/(.*)/$', entrepreneur_view.details_page, name='tenant_customer_entrepreneur_details'),
    url(r'^client/entrepreneur$', entrepreneur_view.master_page, name='tenant_customer_entrepreneur_master'),
)
