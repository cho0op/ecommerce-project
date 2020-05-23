from django.contrib import admin
from analytics.models import ObjectViewed, UserSession

admin.site.register(ObjectViewed)
admin.site.register(UserSession)
# Register your models here.
