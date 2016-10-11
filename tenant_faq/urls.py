from django.conf.urls import include, url
from tenant_faq import views


urlpatterns = (
    url(r'^faq$', views.faq_page, name='tenant_faq'),
)
