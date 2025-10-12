from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag(takes_context=True)
def paginate_url(context, page_number):
    """
    Returns a URL for a given page_number while preserving all other GET parameters
    (like title or author) except 'page'.
    """
    request = context['request']
    get_params = request.GET.copy()
    get_params['page'] = page_number
    return f"?{get_params.urlencode()}"
