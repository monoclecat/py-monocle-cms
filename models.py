from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

from stdimage.models import StdImageField
from stdimage.utils import UploadToClassNameDirUUID
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver

class Image(models.Model):
    file = StdImageField(upload_to=UploadToClassNameDirUUID(), blank=True, variations={
        'large': {"height": 400},
        'medium': {"height": 200},
        'small': {"width": 100, "height": 100, "crop": True},
    })
    tag = models.CharField(max_length=50)
    uploaded = models.DateTimeField(auto_now_add=True)


@receiver(post_delete, sender=Image)
def image_delete(sender, instance, **kwargs):
    if instance.file:
        # Pass false so FileField doesn't save the model.
        instance.file.delete(False)


class Page(models.Model):

    tag = models.CharField(max_length=50)
    created = models.DateField(default=timezone.now)
    admin_only = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    front_page = models.BooleanField(default=False)
    name = models.CharField(default=None, null=True, max_length=30)
    headline = models.CharField(default=None, null=True, max_length=100)
    body = models.TextField(default=None, null=True)

    def slug(self):
        return slugify(self.headline)

    def get_absolute_url(self, edit=False):
        if edit:
            return reverse('py_monocle_cms:content_edit', args=[self.pk, self.slug()])
        else:
            return reverse('py_monocle_cms:content', args=[self.pk, self.slug()])
