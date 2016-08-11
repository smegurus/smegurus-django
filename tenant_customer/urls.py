from django.conf.urls import patterns, include, url
from tenant_customer import views


urlpatterns = (
    url(r'^client/update/(.*)/$', views.update_page, name='tenant_customer_update'),
    url(r'^client/(.*)/$', views.details_page, name='tenant_customer_details'),
    url(r'^client$', views.master_page, name='tenant_customer_master'),
    url(r'^client/create$', views.create_page, name='tenant_customer_create'),
)
