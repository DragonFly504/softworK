from django.contrib import admin
from .models import Shipment, ShipmentEvent


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['tracking_number', 'status', 'sender_name', 'receiver_name', 'origin', 'destination', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['tracking_number', 'origin', 'destination', 'sender_name', 'receiver_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Tracking Info', {'fields': ('tracking_number', 'status')}),
        ('Sender Information', {'fields': ('sender_name', 'sender_email', 'sender_phone')}),
        ('Receiver Information', {'fields': ('receiver_name', 'receiver_email', 'receiver_phone')}),
        ('Package Information', {'fields': ('package_description', 'weight', 'dimensions')}),
        ('Origin Location', {'fields': ('origin', 'origin_lat', 'origin_lng')}),
        ('Destination Location', {'fields': ('destination', 'dest_lat', 'dest_lng')}),
        ('Current Status', {'fields': ('current_location', 'current_lat', 'current_lng')}),
        ('Delivery', {'fields': ('estimated_delivery',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(ShipmentEvent)
class ShipmentEventAdmin(admin.ModelAdmin):
    list_display = ['shipment', 'status', 'location', 'timestamp']
    list_filter = ['status', 'timestamp']
    search_fields = ['shipment__tracking_number', 'status', 'location']
    readonly_fields = ['timestamp']
    
    fieldsets = (
        ('Event Information', {'fields': ('shipment', 'status', 'location')}),
        ('Coordinates', {'fields': ('latitude', 'longitude')}),
        ('Details', {'fields': ('notes', 'timestamp')}),
    )
