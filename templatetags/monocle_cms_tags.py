from django import template
import markdown
from monocle_cms.md_extensions import *

register = template.Library()


@register.filter
def from_markdown(value):
    md = markdown.Markdown(extensions=[PageBuildingExtensions()])
    return md.convert(value)
