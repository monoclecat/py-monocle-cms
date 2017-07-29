from django.conf.urls import url
from django.urls import reverse_lazy
from py_monocle_cms.views import *

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.views.defaults import page_not_found

from .models import Page

languages_regex = '('
for language in Page.languages:
    languages_regex += language + '|'
languages_regex = languages_regex[:-1]
languages_regex += ')'

app_name = 'py_monocle_cms'
urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('py_monocle_cms:index', kwargs={'language': 'en'}))),
    url(r'^image-upload/$', ImageUploadView.as_view(), name='image_upload'),
    url(r'^logout/$', login_view, name='logout'),
    url(r'^login/$', login_view, name='login'),
    url(r'^pages/$', PagesView.as_view(), name='pages'),
    url(r'^edit/(?P<language>'+languages_regex+')/(?P<pk>\d+)/(?P<slug>\S*)$', ContentEditView.as_view(), name='content_edit'),
    url(r'^(?P<language>'+languages_regex+')/(?P<pk>\d+)/(?P<slug>\S*)$', ContentView.as_view(), name='content'),
    url(r'^(?P<language>'+languages_regex+')/$', IndexView.as_view(), name='index'),
    url(r'^about-me/$', TagView.as_view(), kwargs={'language': 'en', 'tag': 'about'}, name='about-en'),
    url(r'^ueber-mich/$', TagView.as_view(), kwargs={'language': 'de', 'tag': 'about'}, name='about-de'),
    url(r'^imprint/$', TagView.as_view(), kwargs={'language': 'en', 'tag': 'imprint'}, name='imprint-en'),
    url(r'^impressum/$', TagView.as_view(), kwargs={'language': 'de', 'tag': 'imprint'}, name='imprint-de'),
    url(r'^404/$', page_not_found, {'exception': Exception('Not Found')}, name='404')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)