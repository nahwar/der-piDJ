from django.contrib import admin
from .models import Search, Image, Details, LogEntry
# Register your models here.
admin.site.register(Search)
admin.site.register(Image)
admin.site.register(Details)
admin.site.register(LogEntry)
