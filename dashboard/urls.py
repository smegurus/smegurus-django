from django.conf.urls import patterns, include, url
from dashboard import views


urlpatterns = (
    url(r'^dashboard$', views.dashboard_page, name='tenant_dashboard'),
    # url(r'^activate/(.*)/(.*)/$', views.activation_page, name='activation'),
)
