#my_markup.py
import markdown
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
register = template.Library()
@register.filter(is_safe=True)
@stringfilter
def my_markdown(value):
    print(value)
    print(force_text(value))
    extensions = ["nl2br","codehilite"]
    return mark_safe(markdown.markdown(force_text(value),
	    extensions,
	    safe_mode=True,
	    enable_attributes=False))