from django import template
from main.models import *
from django.db.models import Q
register = template.Library()

@register.inclusion_tag('main/show_tags.html')
def show_tags():
    components = Component.objects.all().count()
    downloads = Download.objects.all().count()
    contributors = UserProfile.objects.all().count()
    return {'components':components, 'downloads':downloads, 'contributors':contributors,}