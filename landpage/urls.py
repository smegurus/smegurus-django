from django.conf.urls import patterns, include, url
from landpage import views


urlpatterns = (
    url(r'^$', views.land_page, name='landpage'),
    # url(r'^authentication$', views.authentication_page, name='authentication'),
    # url(r'^login$', views.login_page, name='login'),
    # url(r'^register$', views.register_page, name='register'),
    # url(r'^activate/(.*)/(.*)/$', views.activation_page, name='activation'),
)
