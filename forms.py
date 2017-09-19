from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *

import markdown
from py_monocle_cms.md_extensions import *

from .models import Page, Image


class ImageUploadForm(forms.Form):
    class Meta:
        model = Image
        fields = ['image_file_field', 'tag']

    image_file_field = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    tag = forms.CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        super(ImageUploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'page_edit_form'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = 'upload'
        self.helper.layout = Layout(
            'image_file_field',
            'tag',
            FormActions(Submit('upload', 'Upload')),
        )


class PageEditForm(ModelForm):
    class Meta:
        model = Page
        fields = ['tag', 'created', 'admin_only', 'featured', 'front_page', 'name', 'headline', 'body']

    tag = forms.CharField(label='Tag', max_length=50, required=False)
    created = forms.DateField(label='Created', required=False)
    admin_only = forms.BooleanField(label='Only you (the admin) can see this page', required=False)
    featured = forms.BooleanField(label='[Only if tag equals \'project\'] Show in Featured Projects list in sidebar', required=False)
    front_page = forms.BooleanField(label='Show on front page', required=False)
    name = forms.CharField(label='Name', max_length=50, required=False)
    headline = forms.CharField(label='Headline (gets slugged)', max_length=100, required=False)
    body = forms.CharField(label='Body', widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(PageEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'page_edit_form'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = 'save_page'
        self.helper.form_show_labels = True

        md = markdown.Markdown(extensions=[PageBuildingExtensions()])

        if 'instance' in kwargs and kwargs['instance'].headline:
            headline_text = kwargs['instance'].headline
        else:
            headline_text = ""

        if 'instance' in kwargs and kwargs['instance'].body:
            body_text = md.convert(kwargs['instance'].body)
        else:
            body_text = ""

        self.helper.layout = Layout(
            FormActions(Submit('save_done_editing', 'Save and leave edit mode')),
            Field('tag'),
            Field('created', placeholder='YYYY-MM-DD'),
            Field('admin_only'),
            Field('featured'),
            Field('front_page'),
            Field('name'),
            Field('headline'),
            FormActions(Submit('save', 'Save')),
            TabHolder(
                Tab(
                    "Edit",
                    Field('body', rows="100", style="resize: vertical"),
                    FormActions(Submit('save', 'Save'))
                ),
                Tab(
                    "Current content",
                    HTML("<h1>"+headline_text+"</h1>"),
                    HTML(body_text)
                )
            ),

        )
