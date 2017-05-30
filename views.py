from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpRequest, Http404
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic import DetailView
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
    template_name = 'monocle_cms/image_upload.html'
    success_url = '/image-upload'

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


class ContentView(DetailView):
    model = Page
    template_name = 'monocle_cms/page.html'
    context_object_name = 'page'

    def get_object(self, queryset=None):
        page = super(ContentView, self).get_object()
        if page.admin_only and not self.request.user.is_superuser:
            raise Http404
        return page

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ContentView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books

        context['content'], self.kwargs['language'] = context['page'].get_content(self.kwargs['language'])

        context['featured_projects'] = []
        context['other_projects'] = []
        if self.request.user.is_superuser:
            perm_filtered_query = Page.objects.all()
        else:
            perm_filtered_query = Page.objects.all().exclude(admin_only=True)
        if self.kwargs['language'] == 'de':
            try:
                for page in perm_filtered_query.filter(featured=True):
                    context['featured_projects'].append([page.pk, Content.objects.get(pk=page.content_de_id).name])
                for page in perm_filtered_query.filter(featured=False):
                    context['other_projects'].append([page.pk, Content.objects.get(pk=page.content_de_id).name])
            except Page.DoesNotExist:
                pass
        else:
            try:
                for page in perm_filtered_query.filter(featured=True):
                    context['featured_projects'].append([page.pk, Content.objects.get(pk=page.content_en_id).name])
                for page in perm_filtered_query.filter(featured=False):
                    context['other_projects'].append([page.pk, Content.objects.get(pk=page.content_en_id).name])
            except Page.DoesNotExist:
                pass

        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        if context['content'] is None or self.kwargs['slug'] != context['content'].slug():
            # No content was found under the given language or slug was wrong
            return redirect(context['page'].get_absolute_url(self.kwargs['language']))

        return self.render_to_response(context)


class ContentEditView(FormView, ContentView):
    form_class = PageEditForm
    template_name = 'monocle_cms/page_edit.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = ContentView.get_context_data(self, object=self.object)

        self.initial = {'tag': context['page'].tag, 'created': context['page'].created,
                        'admin_only': context['page'].admin_only,
                        'featured': context['page'].featured, 'primary_image': context['page'].primary_image,
                        'other_images': context['page'].other_images, 'name': context['content'].name,
                        'headline': context['content'].headline, 'abstract': context['content'].abstract,
                        'body': context['content'].body}

        context = {**context, **FormView.get_context_data(self, **kwargs)}

        if context['content'] is None or self.kwargs['slug'] != context['content'].slug():
            # No content was found under the given language or slug was wrong
            return redirect(context['page'].get_absolute_url(self.kwargs['language'], True))

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            page = Page.objects.get(pk=self.kwargs['pk'])
            form = PageEditForm(request.POST, instance=page)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save()

        if self.kwargs['language'] == 'de':
            content = Content.objects.get(pk=self.object.content_de_id)
        else:
            content = Content.objects.get(pk=self.object.content_en_id)
        content.name = self.request.POST['name']
        content.headline = self.request.POST['headline']
        content.abstract = self.request.POST['abstract']
        content.body = self.request.POST['body']
        content.save()

        self.success_url = self.object.get_absolute_url(self.kwargs['language'], True)
        return super(ContentEditView, self).form_valid(form)