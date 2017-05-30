"""homepage_django URL Configuration

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
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'monocle_cms'
urlpatterns = [
    url(r'^image-upload/', views.ImageUploadView.as_view(), name='image_upload'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^login/', views.login_view, name='login'),
    url(r'^(?P<language>\S+)/$', views.IndexView.as_view, name='content_no_slug'),
    url(r'^(?P<language>\S+)/(?P<page_pk>\d+)/$', views.content_view, name='content_no_slug'),
    url(r'^(?P<language>\S+)/(?P<page_pk>\d+)/(?P<slug>\S+)$', views.content_view, name='content_slug'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
