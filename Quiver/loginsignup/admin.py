from django.contrib import admin
from .models import Beaver, ResetPasswordModel

# Register your models here.

admin.site.register(Beaver)
admin.site.register(ResetPasswordModel)
