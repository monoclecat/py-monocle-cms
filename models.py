import os
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from django.conf.urls.static import static

from stdimage.models import StdImageField
from stdimage.utils import UploadToClassNameDirUUID


class Image(models.Model):
    file = StdImageField(upload_to=UploadToClassNameDirUUID(), blank=True, variations={
        'large': {"height": 400},
        'medium': {"height": 200},
        'small': {"width": 100, "height": 100, "crop": True},
    })
    tag = models.CharField(max_length=50)
    uploaded = models.DateField(auto_now_add=True)


class Content(models.Model):
    language = models.CharField(default=None, null=True, max_length=10)
    name = models.CharField(default=None, null=True, max_length=30)
    headline = models.CharField(default=None, null=True, max_length=100)
    abstract = models.TextField()
    body = models.TextField()

    def slug(self):
        return slugify(self.headline)


class Page(models.Model):
    tag = models.CharField(max_length=50)
    created = models.DateField(default=timezone.now)
    admin_only = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    primary_image = models.IntegerField(default=None, null=True)
    other_images = models.IntegerField(default=None, null=True)
    content_de = models.ForeignKey(Content, default=None, related_name='page_de', null=True, blank=True)
    content_en = models.ForeignKey(Content, default=None, related_name='page_en', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            # This code only happens if the objects is
            # not in the database yet. Otherwise it would
            # have pk
            new_ger = Content.objects.create(language='de')
            new_eng = Content.objects.create(language='en')
            self.content_en_id = new_eng.pk
            self.content_de_id = new_ger.pk
        super(Page, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        Content.objects.get(pk=self.content_de_id).delete()
        Content.objects.get(pk=self.content_en_id).delete()
        super(Page, self).delete(using=None, keep_parents=False)

    def get_content(self, language):
        if language == 'en':
            return [Content.objects.get(pk=self.content_en_id), language]
        elif language == 'de':
            return [Content.objects.get(pk=self.content_de_id), language]
        else:
            return [None, None]

    def get_absolute_url(self, language='en', edit=False):
        if language == 'en':
            slug = Content.objects.get(pk=self.content_en_id).slug()
        elif language == 'de':
            slug = Content.objects.get(pk=self.content_de_id).slug()
        else:
            raise Exception
        if edit:
            return reverse('monocle_cms:page_edit', args=[language, self.pk, slug])
        else:
            return reverse('monocle_cms:page', args=[language, self.pk, slug])





