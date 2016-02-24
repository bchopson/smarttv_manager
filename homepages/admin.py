from django.contrib import admin

from .models import Tv, Slide

class TvAdmin(admin.ModelAdmin):
    readonly_fields = ('updated',)

admin.site.register(Tv,TvAdmin)
admin.site.register(Slide)