from django.conf.urls import include, url
from public_home import views


urlpatterns = (
    url(r'^$', views.index_page, name='public_home'),
    url(r'^term$', views.term_page, name='public_terms'),
    url(r'^403$', views.http_403_page, name='public_403_error'),
    url(r'^404$', views.http_404_page, name='public_404_error'),
    url(r'^500$', views.http_500_page, name='public_500_error'),
    url(r'^start$', views.start_page, name='public_start'),
)
