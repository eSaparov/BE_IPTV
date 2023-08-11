from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(videos)
admin.site.register(tracks)
admin.site.register(appMetadata)
admin.site.register(storedContent)
