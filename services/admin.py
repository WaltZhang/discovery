from django.contrib import admin

# Register your models here.
from services.models import ServiceModel

admin.site.register(ServiceModel)