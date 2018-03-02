from . import views
from django.conf.urls import url

app_name = 'main'

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^register/?$', views.register, name="register"),
    url(r'^user_login/?$', views.user_login, name="user_login"),
    url(r'^upload_component/?$', views.upload_component, name="upload_component"),
    url(r'^get_user_profile/?$', views.get_user_profile, name="get_user_profile"),
    url(r'^get_profile/(?P<u_id>\d+)/$', views.get_profile, name="get_profile"),
    url(r'^email_confirm/(?P<token>\w+)/$', views.email_confirm, name="email_confirm"),
    url(r'^download_component/(?P<c_id>\d+)/$', views.download_component, name="download_component"),
    url(r'^comment/(?P<c_id>\d+)/$', views.comment, name="comment"),
    url(r'^request_component/?$', views.request_component, name="request_component"),
    url(r'^rate_component/(?P<c_id>\d+)/$', views.rate_component, name="rate_component"),
    url(r'^logout/?$', views.user_logout, name="user_logout"),
]