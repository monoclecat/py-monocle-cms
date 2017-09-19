from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, Http404
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

import logging

from .models import Page, Image
from .forms import PageEditForm, ImageUploadForm


def get_featured_and_other(user_is_admin=False):
    """
    Gives you the primary keys and page names of all Page objects, split up in two arrays: featured_pages and
    non_featured_pages. The sorting is done by the 'featured' field in the model Page.
    To keep out objects that are only meant to be seen by the admin, keep user_is_admin as False.

    :param user_is_admin: If True, Pages with 'admin_only' set to True will be included.
    :return: Array of two arrays containing two-element-arrays. Example: [ [[1, "Contact page"], [2, "Project #1"]], [[4, "Page #3"], [8, "Fun page"]] ]
    """
    featured_pages = []
    non_featured_pages = []

    if user_is_admin:
        perm_filtered_query = Page.objects.all().filter(tag="project")
    else:
        perm_filtered_query = Page.objects.all().filter(tag="project").exclude(admin_only=True)

    for page in perm_filtered_query.filter(featured=True):
        featured_pages.append([page.pk, page.name])
    for page in perm_filtered_query.filter(featured=False):
        non_featured_pages.append([page.pk, page.name])

    return [featured_pages, non_featured_pages]


class TagView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if Page.objects.filter(tag=self.kwargs['tag']).first() is not None:
            about_page_pk = Page.objects.filter(tag=self.kwargs['tag']).first().pk
            self.url = reverse('py_monocle_cms:content', kwargs={'pk': about_page_pk, 'slug': ''})
        else:
            self.url = reverse('py_monocle_cms:404')
        return self.url


class IndexView(ListView):
    model = Page
    template_name = 'py_monocle_cms/index.html'
    context_object_name = 'page'

    def get_queryset(self):
        return Page.objects.all().exclude(admin_only=True).exclude(front_page=False).order_by('-created')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(IndexView, self).get_context_data(**kwargs)
        context['featured_pages'], context['other_pages'] = get_featured_and_other(self.request.user.is_superuser)
        return context


def login_view(request):
    if request.method == 'POST' and 'login' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        return HttpResponseRedirect(request.POST['next'])
    elif request.method == 'POST' and 'logout' in request.POST:
        logout(request)
        return HttpResponseRedirect(request.POST['next'])
    else:
        return render(request, 'py_monocle_cms/login_page.html', {'next': request.GET.get('next', '/login/')})


class ImageUploadView(LoginRequiredMixin, FormView):
    form_class = ImageUploadForm
    template_name = 'py_monocle_cms/image_upload.html'
    success_url = '/image-upload/'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super(ImageUploadView, self).get_context_data(**kwargs)
        sort = self.request.GET.get('sort')

        if sort is None:
            sort = "-"
        sorting_params = sort.split('-', 2)

        if sorting_params[0] not in [f.name for f in Image._meta.get_fields()]:
            sorting_params[0] = 'uploaded'

        if sorting_params[1] == 'asc':
            images = Image.objects.all().order_by(sorting_params[0])
        else:
            images = Image.objects.all().order_by("-"+sorting_params[0])

        context['images'] = images
        context['sort'] = sort
        return context

    def post(self, request, *args, **kwargs):
        if 'delete_single' in request.POST:
            if request.POST['pk'] is not None:
                Image.objects.get(pk=request.POST['pk']).delete()
            else:
                logging.error("request.POST['pk'] is None in ImageUploadView.post() -> delete image")
        elif 'delete_tag' in request.POST:
            for obj in Image.objects.filter(tag=request.POST['tag']):
                obj.delete()
        elif 'upload' in request.POST:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            files = request.FILES.getlist('image_file_field')
            if form.is_valid():
                for f in files:

                    Image.objects.create(file=f, tag=request.POST['tag'])
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        return HttpResponseRedirect(reverse('py_monocle_cms:image_upload'))


class ContentView(DetailView):
    model = Page
    template_name = 'py_monocle_cms/detail_page.html'
    context_object_name = 'page'

    def get_object(self, queryset=None):
        page = super(ContentView, self).get_object()
        if page.admin_only and not self.request.user.is_superuser:
            raise Http404
        return page

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ContentView, self).get_context_data(**kwargs)

        context['featured_pages'], context['other_pages'] = \
            get_featured_and_other(self.request.user.is_superuser)
        return context

    def get(self, request, *args, **kwargs):
        if 'slug' not in self.kwargs:
            self.kwargs['slug'] = ''

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        if self.kwargs['slug'] != context['page'].slug():
            return redirect(context['page'].get_absolute_url())
        return self.render_to_response(context)


class ContentEditView(LoginRequiredMixin, FormView, ContentView):
    form_class = PageEditForm
    template_name = 'py_monocle_cms/edit_page.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        context = ContentView.get_context_data(self, object=self.object)

        form = PageEditForm(instance=self.object)

        context['form'] = form

        if self.kwargs['slug'] != context['page'].slug():
            return redirect(context['page'].get_absolute_url(True))

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            page = Page.objects.get(pk=self.kwargs['pk'])
            form = PageEditForm(request.POST, instance=page)
            if 'save_done_editing' in request.POST:
                edit_mode = False
            else:
                edit_mode = True
            return self.form_valid(form, edit_mode)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, edit_mode=True):
        self.object = form.save()
        self.success_url = self.object.get_absolute_url(edit_mode)
        return super(ContentEditView, self).form_valid(form)


class PagesView(LoginRequiredMixin, ListView):
    model = Page
    template_name = 'py_monocle_cms/pages.html'
    context_object_name = 'page'
    login_url = '/login/'

    def get_queryset(self):
        return Page.objects.all().order_by('-created')

    def post(self, request, *args, **kwargs):
        if 'new' in request.POST:
            Page.objects.create()
        elif 'delete' in request.POST:
            if request.POST['pk'] is not None:
                Page.objects.get(pk=request.POST['pk']).delete()
            else:
                logging.error("request.POST['pk'] is None in PagesView.post() -> delete page")
        return HttpResponseRedirect(reverse('py_monocle_cms:pages'))
