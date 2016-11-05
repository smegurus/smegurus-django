from django.conf.urls import include, url
from tenant_bizmula.views import stage_view, module_view


urlpatterns = (
    url(r'^workspace/(.*)/exercise/(.*)/question/(.*)/$', exercise_view.detail_page, name='tenant_workspace_exercise_detail'),
)
