from django import template

register = template.Library()

@register.filter
def calu(num):
    return int(num/100)

@register.filter
def jian(num):
    return num-1