from django.contrib import admin
from .models import product, Contact, Orders, OrderUpdate
# Register your models here.

admin.site.register(product)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('msg_id','name','email','phone')
    search_fields = ('name','email')
admin.site.register(Contact,ContactAdmin)

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'name', 'email', 'city', 'state', 'amount')
    search_fields = ('order_id', 'name', 'email', 'phone', 'city', 'state', 'zip_code')
    list_filter = ('state', 'city')
    ordering = ('-order_id',)

admin.site.register(Orders,OrdersAdmin)

class OrderUpdateAdmin(admin.ModelAdmin):
    list_display = ('update_id', 'order_id', 'update_desc', 'timestamp')
    search_fields = ('order_id', 'update_desc')
    list_filter = ('timestamp',)
    ordering = ('update_id',)
admin.site.register(OrderUpdate,OrderUpdateAdmin)