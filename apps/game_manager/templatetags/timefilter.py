#coding:utf-8
import time
from django import template
register = template.Library()

@register.filter('timefilter')
def timefilter(value):
    """
    时间格式化
    """
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(value))