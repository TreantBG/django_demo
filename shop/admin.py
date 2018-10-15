from django.contrib import admin

from .models import Category, Product, Order


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name']


class OrderAdmin(admin.ModelAdmin):
    search_fields = ['user__username']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
