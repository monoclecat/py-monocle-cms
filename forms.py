from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import FormActions

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
        fields = ['tag', 'created', 'admin_only', 'featured', 'name', 'headline', 'abstract', 'body']
    tag = forms.CharField(label='Tag', max_length=50, required=False)
    created = forms.DateField(label='Created', required=False)
    admin_only = forms.BooleanField(label='Admin only', required=False)
    featured = forms.BooleanField(label='Featured', required=False)
    name = forms.CharField(label='Name', max_length=50, required=False)
    headline = forms.CharField(label='Headline (gets slugged)', max_length=100, required=False)
    abstract = forms.CharField(label='Abstract', widget=forms.Textarea, required=False)
    body = forms.CharField(label='Body', widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(PageEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'page_edit_form'
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = 'save_page'

        self.helper.layout = Layout(
            'tag',
            'created',
            'admin_only',
            'featured',
            'name',
            'headline',
            'abstract',
            'body',
            FormActions(Submit('save', 'Save')),
        )
