from django.contrib import admin
from .models import Task
from .models import Comment, Statuses, History_changed

admin.site.register(Task)
admin.site.register(Comment)

# admin.site.register(History_changed)
# Register your models here.

class MyModelAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "title":
            kwargs["queryset"] = Statuses.objects.order_by('sort')
        return super(MyModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Statuses)