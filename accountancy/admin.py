from django.contrib import admin

# Register your models here.
from .models import File, Class, Group, Note
admin.site.register(File)
admin.site.register(Class)
admin.site.register(Group)
admin.site.register(Note)