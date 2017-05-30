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
from monocle_cms.views import *

from django.conf import settings
from django.conf.urls.static import static

app_name = 'monocle_cms'
urlpatterns = [
    url(r'^image-upload/', ImageUploadView.as_view(), name='image_upload'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^login/', views.login_view, name='login'),

    url(r'^edit/(?P<language>\S+)/(?P<pk>\d+)/(?P<slug>\S*)$', login_required(ContentEditView.as_view()), name='page_edit'),
    url(r'^(?P<language>\S+)/(?P<pk>\d+)/(?P<slug>\S+)$', ContentView.as_view(), name='page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
