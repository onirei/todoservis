from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.task_list,  name='tasks'),
    url(r'^change/$', views.change, name='change'),
    url(r'^statistic/$', views.statistic, name='statistic'),
    # url(r'^register/$', views.RegisterFormView.as_view()),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.logout, name='logout'),

]
