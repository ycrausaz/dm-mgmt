from django.contrib import admin

from .models import Client
from .models import Massage
from .models import Service

class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_last_name', 'client_first_name', 'client_birthdate')
    fields = (('client_first_name', 'client_last_name'), 'client_birthdate', ('client_address'), ('client_zip_code', 'client_city'), ('client_phone_number_1', 'client_phone_number_2'), 'client_email_address', 'client_comment')
    ordering = ('client_last_name', 'client_first_name',)
    search_fields = ('client_first_name', 'client_last_name')
    pass


class MassageAdmin(admin.ModelAdmin):
    pass


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_date', 'service_client_id', 'service_massage_id', 'service_duration', 'service_cashed_price')
    fields = ('service_client_id', 'service_massage_id', 'service_date', ('service_duration', 'service_cashed_price'), 'service_comment')
    ordering = ('-service_date',)
    search_fields = ('service_client_id',)
    list_filter = ('service_date',)
    # readonly_fields = ('service_cashed_price',)
    pass


admin.site.register(Client, ClientAdmin)
admin.site.register(Massage, MassageAdmin)
admin.site.register(Service, ServiceAdmin)
