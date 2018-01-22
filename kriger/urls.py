"""kriger URL Configuration

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

from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/$',views.CreateUserView.as_view()),
    url(r'^users/',views.UserList.as_view()),
    url(r'^activate_link/(?P<code>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z_\-]+)',views.verify_link,name='verify'),
    url(r'^send/',views.SendConfirmation.as_view(),name='send'),
    url(r'^uploademail/',views.UploademailAPIView.as_view()),
    url(r'^getuploademail',views.GetUploademailAPIView.as_view()),
    url(r'^uploadphone/',views.UploadphoneAPIView.as_view()),
    url(r'^getuploadphone/',views.GetUploadphoneAPIView.as_view()),
    url(r'^storereceiverequest/',views.storereceivereqAPIView.as_view()),
    url(r'^getreceiverequest/',views.getreceivereqAPIView.as_view()),
    url(r'^createpost/',views.createpostAPIView.as_view()),
    url(r'^likespost/',views.likecreatedAPIView.as_view()),
    url(r'^postlike/(?P<titleofpost>.+)/$',views.numoflikes.as_view()),  #lists number of likes on post
url(r'^sharepost/',views.shareAPIView.as_view()),
    url(r'^postshare/(?P<titleofpost>.+)/$', views.numofshares.as_view()),
]
