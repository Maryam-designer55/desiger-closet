from django.contrib import admin
from .models import Product, Order, OrderItem

# 1. Product Admin Configuration
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    search_fields = ('name',)

# 2. OrderItems ko Order ke andar inline dikhane ke liye
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

# 3. Order Admin Configuration
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'phone_number', 'shipping_address', 'created_at']
    list_filter = ['created_at']
    inlines = [OrderItemInline]  # Is se admin panel mein order ke andar hi saare items nazar aayenge