"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from blog import views
from accounts import views as av
from accounts.views import  activation_sent_view, activate
from django.contrib.auth import views as auth_views
urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^$', views.post_list_view,name="post_list"),
    url(r'^tag/(?P<tag_slug>[\w]+)/$', views.post_list_view, name='post_list_by_tag_name'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$', views.post_detail_view,name='post_detail'),
    url(r'^(?P<my_id>\d+)/share/$', views.mail_send_view),
    url(r'^home/', views.home_view, name="write"),
    url(r'^login/',av.login_view,name="login"),
    url(r"^register/", av.ragister_view, name="ragister"),
    url(r"^logout/", av.logout_view, name="logout"),
    url(r'^sent/', av.activation_sent_view, name="activation_sent"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,23})/$', av.activate, name='activate'),
    url(r'^password_reset/$', auth_views.password_reset,{
            "template_name": "accounts/password_reset_form.html"
        },name="password_reset"),
    url(r'^password_reset/done/$', auth_views.password_reset_done,{
            "template_name": "accounts/password_reset_done.html"
        },name="password_reset_done"),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    auth_views.password_reset_confirm,{
            "template_name": "accounts/password_reset_confirm.html"
        },name="password_reset_confirm"),
    url(r'^reset/done/$', auth_views.password_reset_complete,{
            "template_name": "accounts/password_reset_complete.html"
        },name="password_reset_complete"),
]

 #http://127.0.0.1:8000/activate/MTk/5gj-3605e2d913e9232e449f/
 #http://127.0.0.1:8000/activate/MTQ/5gj-51bcb7872dbbdea63e23/
 #http://127.0.0.1:8000/activate/MjA/5gj-8f9b81601903feca20e8/
