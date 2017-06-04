from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

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
    languages = ['en', 'de']

    tag = models.CharField(max_length=50)
    created = models.DateField(default=timezone.now)
    admin_only = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    content = models.ManyToManyField(Content, default=None)

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Page, self).save(*args, **kwargs)
            for language in self.languages:
                new_content = Content.objects.create(language=language)
                self.content.add(new_content)
        else:
            super(Page, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        for content in self.content.all():
            content.delete()
        super(Page, self).delete(using=None, keep_parents=False)

    def get_absolute_url(self, language=languages[0], edit=False):
        try:
            slug = self.content.get(language=language).slug()
        except Content.DoesNotExist:
            slug = ''
        if edit:
            return reverse('monocle_cms:content_edit', args=[language, self.pk, slug])
        else:
            return reverse('monocle_cms:content', args=[language, self.pk, slug])
