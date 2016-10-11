from django.conf.urls import include, url
from tenant_mywork import views


urlpatterns = (
    url(r'^mywork$', views.mywork_page, name='tenant_mywork'),
)
