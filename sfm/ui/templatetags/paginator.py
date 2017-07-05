from django import template

register = template.Library()


@register.inclusion_tag('ui/pagination_snippet.html')
def sfm_paginator(page, page_suffix='', page_mid_range=5):
    """
    return google like pagination
    Usage::
        {% sfm_paginator the_obj_to_paginate %}
    Example::
        {% sfm_paginator harvest_list %}
        :param page: page object needs to pagination
        :param page_mid_range: how many page show in the mid parts
        :param page_suffix: page suffix to make multi page indexes in one page
    """
    # Get the index of the current page
    index = page.number - 1
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(page.paginator.page_range)
    page_diff = page_mid_range / 2
    page_addition = 1 if page_mid_range % 2 == 1 else 0
    start_index = index - page_diff if index >= page_diff else 0
    if start_index < page_diff:
        end_index = min(max_index, start_index + page_mid_range)
    else:
        end_index = index + page_diff + page_addition if index <= max_index - page_diff - page_addition else max_index
    # My new page range
    page_range = page.paginator.page_range[start_index:end_index]

    return {
        'page': page,
        'suffix': page_suffix,
        'page_range': page_range
    }
