from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem

# Register ShippingAddress and OrderItem normally
admin.site.register(ShippingAddress)
admin.site.register(OrderItem)


class OrderItemInline(admin.StackedInline):
	model = OrderItem
	extra = 0


class OrderAdmin(admin.ModelAdmin):
	model = Order
	readonly_fields = ['order_date']
	inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
