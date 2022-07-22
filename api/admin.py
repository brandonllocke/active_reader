from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Book, Reading

admin.site.register(User, UserAdmin)
admin.site.register(Book)
admin.site.register(Reading)
