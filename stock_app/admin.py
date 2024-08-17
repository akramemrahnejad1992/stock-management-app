from django.contrib import admin

from .models import Stock, UserStock

admin.site.register(Stock)
admin.site.register(UserStock)
