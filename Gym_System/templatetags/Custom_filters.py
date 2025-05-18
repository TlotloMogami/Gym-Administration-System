from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0)  # returns 0 if key not found
