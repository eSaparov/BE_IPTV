from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group

admin.site.register(User)
admin.site.register(videos)
admin.site.register(tracks)
admin.site.register(appMetadata)
admin.site.register(storedContent)
admin.site.unregister(Group)
