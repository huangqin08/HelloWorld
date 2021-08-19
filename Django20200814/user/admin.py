from django.contrib import admin

# Register your models here.
from user.models import UserType,User

admin.site.register(UserType)
admin.site.register(User)
