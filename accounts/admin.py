from django.contrib import admin
from .models import profile, Group, group_message, message, Notification
# Register your models here.

admin.site.register(profile)
admin.site.register(Group)
admin.site.register(group_message)
admin.site.register(message)
admin.site.register(Notification)

