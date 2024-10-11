from django.contrib import admin
from .models import OcrAws

# Register your models here.
class AdminOcrAws(admin.ModelAdmin):
    list_display = ('id', 'image', 'text', )
    
admin.site.register(OcrAws, AdminOcrAws)