from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpRequest, Http404
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

import markdown


import logging

from .md_extensions import *
from .models import Page, Content, Image
from .forms import PageEditForm, ImageUploadForm


class IndexView(ListView):
    pass


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            error_message = 'Login successful!'
            login_success = True
        else:
            error_message = 'Login failed.'
            login_success = False
        return render(request, 'monocle_cms/login_page.html',
                      {'error_message': error_message, 'login_success': login_success})
    else:
        return render(request, 'monocle_cms/login_page.html')


def logout_view(request):
    if request.method == 'POST' and request.user.is_superuser:
        logout(request)
        return HttpResponseRedirect(request.POST['submitted_from'])


class ImageUploadView(FormView):
    form_class = ImageUploadForm
    template_name = 'monocle_cms/image_upload.html'  # Replace with your template.
    success_url = '/image-upload' # Replace with your URL or reverse().

    def get_context_data(self, **kwargs):
        context = super(ImageUploadView, self).get_context_data(**kwargs)
        images = Image.objects.all()
        context['images'] = images
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('image_file_field')
        if form.is_valid():
            for f in files:
                Image.objects.create(file=f, tag=request.POST['tag'])
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def content_view(request, language, page_pk, slug=None):
    if request.method == 'POST' and request.user.is_superuser:
        try:
            page = Page.objects.get(pk=page_pk)
            page_form = PageEditForm(request.POST, instance=page)
            try:
                page = page_form.save()
            except ValueError:
                raise Exception #TODO add handler
        except Page.DoesNotExist:
            page_form = PageEditForm(request.POST)
            try:
                page = page_form.save()
            except ValueError:
                raise Exception  # TODO add handler

        if language == 'de':
            content = Content.objects.get(pk=page.content_de_id)
        else:
            content = Content.objects.get(pk=page.content_en_id)
        content.name = request.POST['name']
        content.headline = request.POST['headline']
        content.abstract = request.POST['abstract']
        content.body = request.POST['body']
        content.save()

        return HttpResponseRedirect(reverse('monocle_cms:content_slug',
                                            args=[language, page_pk, page.slug(language)]))
    else:
        # first get the object
        if request.user.is_superuser:
            try:
                page = Page.objects.get(pk=page_pk)
            except Page.DoesNotExist:
                page = Page.objects.create()
                return HttpResponseRedirect(reverse('monocle_cms:content_no_slug',
                                                    args=[language, page.pk]))
        else:
            page = get_object_or_404(Page, pk=page_pk)

        if page.admin_only and not request.user.is_superuser:
            raise Http404

        if language != 'en' and language != 'de':
            return redirect(page.get_absolute_url())

        # Now we will check if the slug in url is same
        # as my_object's slug or not
        if slug != page.slug(language):
            # either slug is wrong or None
            return redirect(page.get_absolute_url(language))

        featured_projects = []
        other_projects = []
        if request.user.is_superuser:
            perm_filtered_query = Page.objects.all()
        else:
            perm_filtered_query = Page.objects.all().exclude(admin_only=True)

        if language == 'de':
            content = Content.objects.get(pk=page.content_de_id)
            try:
                for page in perm_filtered_query.filter(featured=True):
                    featured_projects.append([page.pk, Content.objects.get(pk=page.content_de_id).name])
                for page in perm_filtered_query.filter(featured=False):
                    other_projects.append([page.pk, Content.objects.get(pk=page.content_de_id).name])
            except Page.DoesNotExist:
                pass
        else:
            content = Content.objects.get(pk=page.content_en_id)
            try:
                for page in perm_filtered_query.filter(featured=True):
                    featured_projects.append([page.pk, Content.objects.get(pk=page.content_en_id).name])
                for page in perm_filtered_query.filter(featured=False):
                    other_projects.append([page.pk, Content.objects.get(pk=page.content_en_id).name])
            except Page.DoesNotExist:
                pass

        form = PageEditForm(initial=
                            {'tag': page.tag, 'created': page.created, 'admin_only': page.admin_only,
                             'featured': page.featured, 'primary_image': page.primary_image,
                             'other_images': page.other_images, 'name': content.name,
                             'headline': content.headline, 'abstract': content.abstract,
                             'body': content.body}, instance=page)

        md = markdown.Markdown(extensions=[PageBuildingExtensions()])
        html = md.convert(content.body)
        if request.user.is_superuser:
            return render(request, 'monocle_cms/content_page_edit.html',
                          {'page': page, 'content': content, 'form': form,
                           'featured_projects': featured_projects, 'other_projects': other_projects,
                           'language': language, 'html_content_body': html})
        else:
            content.body = html
            return render(request, 'monocle_cms/content_page.html',
                          {'page': page, 'content': content,
                           'featured_projects': featured_projects, 'other_projects': other_projects,
                           'language': language})
