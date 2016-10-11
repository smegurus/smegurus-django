from django.conf.urls import include, url
from tenant_dashboard import views


urlpatterns = (
    url(r'^dashboard$', views.dashboard_page, name='tenant_dashboard'),
    # url(r'^activate/(.*)/(.*)/$', views.activation_page, name='activation'),
)
