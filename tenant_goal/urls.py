from django.conf.urls import patterns, include, url
from tenant_goal import views


urlpatterns = (
    url(r'^goal$', views.goal_page, name='tenant_goal'),
)
