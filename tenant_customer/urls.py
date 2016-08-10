from django.conf.urls import patterns, include, url
from tenant_customer import views


urlpatterns = (
    url(r'^client$', views.master_page, name='tenant_customer_master'),
    url(r'^client/(.*)/$', views.details_page, name='tenant_customer_details'),
    url(r'^client/create$', views.create_page, name='tenant_customer_create'),
    url(r'^client/update/(.*)/1$', views.update_1_page, name='tenant_customer_update_1'),
    url(r'^client/update/(.*)/2$', views.update_2_page, name='tenant_customer_update_2'),
)
