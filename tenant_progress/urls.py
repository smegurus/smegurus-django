from django.conf.urls import patterns, include, url
from tenant_progress import views


urlpatterns = (
    url(r'^progress$', views.progress_page, name='tenant_progress'),
)
