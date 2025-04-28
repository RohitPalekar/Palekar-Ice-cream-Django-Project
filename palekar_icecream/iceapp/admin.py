from django.contrib import admin
from iceapp.models import IcecreamInfo
# Register your models here.

class IcecreamInfoAdmin(admin.ModelAdmin):
    list_display = ['id','iname','category','price'] # --> it disply's all columns from list on admin panel for product

    # to add filter on admin prodct table's panel add below list
    list_filter=['category']

admin.site.register(IcecreamInfo,IcecreamInfoAdmin)