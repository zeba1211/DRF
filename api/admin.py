from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from silk.models import Profile, SQLQuery, Request

admin.site.register(Profile)
admin.site.register(SQLQuery)
admin.site.register(Request)

