from django.contrib import admin
from .models import *  # importing all of our model classes

# Register your models here.

# Denise and Kevin
admin.site.register(UserProfile)
admin.site.register(Request)
admin.site.register(HardDrive)
admin.site.register(Event)
admin.site.register(Log)
admin.site.register(Amendment)
# Kevin - Configurations
admin.site.register(RequestStatusChoice)
admin.site.register(RequesterStatusChoice)
admin.site.register(MaintainerStatusChoice)
admin.site.register(AuditorStatusChoice)
admin.site.register(EventStatusChoice)
admin.site.register(EventDurationChoice)
admin.site.register(EventTypeChoice)
admin.site.register(HardDriveClassificationChoice)
admin.site.register(HardDriveBootTestStatusChoice)
admin.site.register(HardDriveSizeChoice)
