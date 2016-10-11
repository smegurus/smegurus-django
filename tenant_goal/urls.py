from django.conf.urls import include, url
from tenant_goal import views


urlpatterns = (
    url(r'^goal$', views.goal_page, name='tenant_goal'),
)
