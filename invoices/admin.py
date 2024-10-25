from django.contrib import admin
from .models import Client, Service, Invoice, Profile


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'first_name',
        'last_name',
        'email_address',
        'mobile_number',
        'city',
        'country',
        'created_date',
        'updated_date',
        'slug',
        'author',
    ]

    list_filter = ['country', 'city', ]

    search_fields = ['email_address', 'mobile_number', ]

    ordering = ['-created_date']


admin.site.register(Service)
admin.site.register(Invoice)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'first_name',
        'last_name',
        'email_address',
        'mobile_number',
        'city',
        'country',
        'author',
    ]

    list_filter = ['country', 'city', ]

    search_fields = ['email_address', 'mobile_number', ]
