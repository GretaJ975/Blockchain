from django.contrib import admin

from .models import Order, CreateMine, Profile


class BlockchainEntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_added')  # Columns to display in the list view
    search_fields = ('name',)  # Add a search box for the 'name' field
    list_filter = ('date_added',)  # Add a filter by 'date_added'

admin.site.site_header = "Blockchain Administration"
admin.site.site_title = "Blockchain Admin Panel"
admin.site.index_title = "Welcome to Blockchain Administration"


class CreateMineAdmin(admin.ModelAdmin):
    list_display = ("id", "timestamp", "previous_hash", "hash", "data")
    search_fields = ("id", "previous_hash", "hash")
    ordering = ("-timestamp",)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'order_date')
    search_fields = ('customer_name', 'product_name')
    list_filter = ('order_date',)

admin.site.register(Order,OrderAdmin)
admin.site.register(CreateMine)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_pic')
    list_filter = ( 'user', )

admin.site.register(Profile, ProfileAdmin)
