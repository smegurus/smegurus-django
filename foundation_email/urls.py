from django.conf.urls import patterns, include, url
from foundation_email import views


urlpatterns = (
    url(r'^email/auth/activate$', views.activate_page, name='foundation_email_activate'),
)
