from django.conf.urls import url
from django.urls import reverse_lazy
from monocle_cms.views import *

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.views.defaults import page_not_found

languages_regex = '('
for language in Page.languages:
    languages_regex += language + '|'
languages_regex = languages_regex[:-1]
languages_regex += ')'

app_name = 'monocle_cms'
urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('monocle_cms:index', kwargs={'language': 'en'}))),
    url(r'^image-upload/$', ImageUploadView.as_view(), name='image_upload'),
    url(r'^logout/$', login_view, name='logout'),
    url(r'^login/$', login_view, name='login'),
    url(r'^pages/$', AdminView.as_view(), name='admin'),
    url(r'^edit/(?P<language>'+languages_regex+')/(?P<pk>\d+)/(?P<slug>\S*)$', ContentEditView.as_view(), name='content_edit'),
    url(r'^(?P<language>'+languages_regex+')/(?P<pk>\d+)/(?P<slug>\S*)$', ContentView.as_view(), name='content'),
    url(r'^(?P<language>'+languages_regex+')/$', IndexView.as_view(), name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if Page.objects.filter(tag='about').first() is not None:
    about_page_pk = Page.objects.filter(tag='about').first().pk
    urlpatterns += [url(r'^about-me/$', RedirectView.as_view(
        url=reverse_lazy('monocle_cms:content', kwargs={'pk': about_page_pk, 'language': 'en', 'slug': ''})),
        name='about-en')]
    urlpatterns += [url(r'^ueber-mich/$', RedirectView.as_view(
        url=reverse_lazy('monocle_cms:content', kwargs={'pk': about_page_pk, 'language': 'de', 'slug': ''})),
        name='about-de')]
else:
    urlpatterns += [url(r'^about-me/$', page_not_found, {'exception': Exception('Not Found')}, name='about-en')]
    urlpatterns += [url(r'^ueber-mich/$', page_not_found, {'exception': Exception('Not Found')}, name='about-de')]

if Page.objects.filter(tag='impressum').first() is not None:
    impressum_page_pk = Page.objects.filter(tag='impressum').first().pk
    urlpatterns += [url(r'^imprint/$', RedirectView.as_view(
        url=reverse_lazy('monocle_cms:content', kwargs={'pk': impressum_page_pk, 'language': 'en', 'slug': ''})),
        name='impressum-en')]
    urlpatterns += [url(r'^impressum/$', RedirectView.as_view(
        url=reverse_lazy('monocle_cms:content', kwargs={'pk': impressum_page_pk, 'language': 'de', 'slug': ''})),
        name='impressum-de')]
else:
    urlpatterns += [url(r'^imprint/$', page_not_found, {'exception': Exception('Not Found')}, name='impressum-en')]
    urlpatterns += [url(r'^impressum/$', page_not_found, {'exception': Exception('Not Found')}, name='impressum-de')]
