from django.contrib import admin
from .models import Shipment, ShipmentEvent


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['tracking_number', 'status', 'origin', 'destination', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['tracking_number', 'origin', 'destination']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Tracking Info', {'fields': ('tracking_number', 'status')}),
        ('Locations', {'fields': ('origin', 'destination', 'origin_lat', 'origin_lng', 'dest_lat', 'dest_lng', 'current_lat', 'current_lng')}),
        ('Package Info', {'fields': ('weight', 'dimensions')}),
        ('Delivery', {'fields': ('estimated_delivery',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(ShipmentEvent)
class ShipmentEventAdmin(admin.ModelAdmin):
    list_display = ['shipment', 'status', 'timestamp']
    list_filter = ['status', 'timestamp']
    search_fields = ['shipment__tracking_number', 'status']
    readonly_fields = ['timestamp']
