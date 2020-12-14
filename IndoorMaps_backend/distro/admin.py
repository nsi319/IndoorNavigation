from django.contrib import admin
from distro.models import *
class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ('date','enters', 'exits')



# Register your models here.
admin.site.register(Dist, RatingAdmin)
admin.site.register(ReferencePoint)
admin.site.register(Offers)
