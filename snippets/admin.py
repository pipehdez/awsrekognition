from django.contrib import admin
from .models import Snippet

class AdminSnippet(admin.ModelAdmin):
    list_display = ('id', 'title', 'code', 'linenos', 'language', 'style', )

admin.site.register(Snippet, AdminSnippet)