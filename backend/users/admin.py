from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Subscriber

admin.site.register(CustomUser, UserAdmin)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    # list_filter = ('name',)

