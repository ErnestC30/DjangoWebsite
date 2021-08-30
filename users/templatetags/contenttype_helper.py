from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.filter
def return_object(content):
    #Return the object associated with the given Content object
    if not content:
        return False
    return content.content_type.get_object_for_this_type(id=content.object_id) 

