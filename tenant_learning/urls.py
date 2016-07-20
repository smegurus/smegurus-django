from django.conf.urls import patterns, include, url
from tenant_learning import views


urlpatterns = (
    url(r'^learning$', views.learning_page, name='tenant_learning'),
)
