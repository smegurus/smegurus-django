import re
from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter
@stringfilter
def urlify_external_links(value):
    """
    Template will take all URL based text and create a <a></a> html associated with it.
    """
    # Regex taken from: http://stackoverflow.com/a/6883094 to find HTTP URLs.
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', value)

    # Iterate through all the URLs we've found and replace it with
    # <a href=""> HTML element code to it.
    for url in urls:
        new_url = "<a href=\""+url+"\" target=\"_blank\">"+url+"</a>"  # Make external link.
        value = value.replace(url, new_url)
    return value.lower()
