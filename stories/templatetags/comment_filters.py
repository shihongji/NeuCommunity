# Since we're handling the ordering and filtering of root comments in the view, we no longer need the custom filter.
from django import template

register = template.Library()


@register.filter
def filter_parent_comments(comments):
    return comments.filter(parent_comment__isnull=True)
