from django.conf.urls import url
from django.urls import reverse_lazy
from py_monocle_cms.views import *

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.views.defaults import page_not_found

app_name = 'py_monocle_cms'
urlpatterns = [
    url(r'^$',  IndexView.as_view(), name='index'),
    url(r'^image-upload/$', ImageUploadView.as_view(), name='image_upload'),
    url(r'^logout/$', login_view, name='logout'),
    url(r'^login/$', login_view, name='login'),
    url(r'^pages/$', PagesView.as_view(), name='pages'),
    url(r'^edit/(?P<pk>\d+)/(?P<slug>\S*)$', ContentEditView.as_view(), name='content_edit'),
    url(r'^(?P<pk>\d+)/(?P<slug>\S*)$', ContentView.as_view(), name='content'),
    url(r'^about-me/$', TagView.as_view(), kwargs={'tag': 'about'}, name='about'),
    url(r'^imprint/$', TagView.as_view(), kwargs={'tag': 'imprint'}, name='imprint'),
    url(r'^404/$', page_not_found, {'exception': Exception('Not Found')}, name='404')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)