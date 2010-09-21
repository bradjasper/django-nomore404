from django.contrib import admin
import models

class PatternAdmin(admin.ModelAdmin):
    list_display  = ('regex', 'description')
    search_fields = ('regex', 'description')

class ErrorAdmin(admin.ModelAdmin):
    list_display  = ('path',)
    search_fields = ('path', 'request')

admin.site.register(models.Pattern, PatternAdmin)
admin.site.register(models.ErrorRequest, ErrorAdmin)
