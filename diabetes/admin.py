from django.contrib import admin

from diabetes.models import UserProfile, GlucoseData

admin.site.register(UserProfile)
admin.site.register(GlucoseData)
