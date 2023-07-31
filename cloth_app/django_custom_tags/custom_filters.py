# custom_filters.py

from django import template

register = template.Library()

@register.filter
def unique_colors(variants):
    unique_colors_list = []
    for variant in variants:
        if variant.get('color') and variant['color'] not in unique_colors_list:
            unique_colors_list.append(variant['color'])
    return unique_colors_list
