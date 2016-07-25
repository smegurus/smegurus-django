from django.conf.urls import patterns, include, url
from public_index import views


urlpatterns = (
    url(r'^$', views.index_page, name='public_index'),
    url(r'^term$', views.term_page, name='public_terms'),
)
