from django.conf.urls import patterns, include, url
from tenant_customer import views


urlpatterns = (
    url(r'^client/update/(.*)/$', views.update_page, name='tenant_customer_update'),
    url(r'^client/(.*)/create/step-3$', views.create_step_three_page, name='tenant_customer_create_step_3'),
    url(r'^client/(.*)/create/step-2$', views.create_step_two_page, name='tenant_customer_create_step_2'),
    url(r'^client/(.*)/create/step-1$', views.create_step_one_page, name='tenant_customer_create_step_1'),
    url(r'^client/create$', views.create_page, name='tenant_customer_create'),
    url(r'^client/(.*)/$', views.details_page, name='tenant_customer_details'),
    url(r'^client$', views.master_page, name='tenant_customer_master'),
)
