from django.conf.urls import include, url
from tenant_reward import views


urlpatterns = (
    url(r'^reward$', views.reward_page, name='tenant_reward'),
)
