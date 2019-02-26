from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.task_list,  name='task_list'),
    url(r'^change/$', views.change, name='change'),
    url(r'^statistic/$', views.statistic, name='statistic'),
    # url(r'^register/$', views.RegisterFormView.as_view()),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/', views.logout_view, name='logout'),

]
