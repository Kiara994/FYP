from django.contrib import admin

from erp.billing.models import Billing, Insurance

# Register your models here.
admin.site.register(Billing)
admin.site.register(Insurance)
