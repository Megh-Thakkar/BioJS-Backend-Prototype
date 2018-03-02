from django.contrib import admin

from .models import *

admin.site.register(UserProfile)
admin.site.register(Component)
admin.site.register(Comment)
admin.site.register(Download)