from django.conf.urls import include, url
from tenant_review import views


urlpatterns = (
    url(r'^document_review/(.*)/$', views.detail_page, name='tenant_review_detail'),
    url(r'^document_review$', views.master_page, name='tenant_review_master'),
)
