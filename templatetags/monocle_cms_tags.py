from django import template
import markdown
from py_monocle_cms.md_extensions import *

register = template.Library()


@register.filter
def from_markdown(value):
    md = markdown.Markdown(extensions=[PageBuildingExtensions()])
    if value:
        return md.convert(value)
    else:
        return ""

@register.filter
def from_md_no_img(value):
    md = markdown.Markdown(extensions=[NoImgExtension()])
    if value:
        return md.convert(value)
    else:
        return ""

@register.filter
def from_md_first_img(value):
    md = markdown.Markdown(extensions=[FirstImgExtension()])
    if value:
        return md.convert(value)
    else:
        return ""


