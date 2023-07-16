from django.contrib import admin
from .models import Property

class PopertyAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not change:
            # the object is being created, so set the user
            obj.publisher = request.user
            form.publisher = request.user
        obj.save()

# Register your models here.
admin.site.register(Property, PopertyAdmin)