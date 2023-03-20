from django import template


register = template.Library()


@register.filter
def first_two_tags(tags):
    return ', '.join(tag.name for tag in tags.all()[:2])
