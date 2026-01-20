from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Shipment, ShipmentEvent
import uuid


class ShipmentEventInline(admin.TabularInline):
    """Inline admin for adding/editing events directly on shipment page"""
    model = ShipmentEvent
    extra = 1  # Show 1 empty form for adding new events
    fields = ['status', 'location', 'latitude', 'longitude', 'notes', 'timestamp']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    
    def get_readonly_fields(self, request, obj=None):
        # Allow editing timestamp on new events
        if obj is None:
            return []
        return ['timestamp']


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = [
        'tracking_number', 
        'status_badge', 
        'sender_name', 
        'receiver_name', 
        'origin', 
        'destination', 
        'progress_display',
        'estimated_delivery',
        'created_at'
    ]
    list_filter = ['status', 'created_at', 'estimated_delivery']
    search_fields = ['tracking_number', 'origin', 'destination', 'sender_name', 'receiver_name', 'sender_email', 'receiver_email']
    readonly_fields = ['created_at', 'updated_at', 'progress_display', 'tracking_link']
    date_hierarchy = 'created_at'
    list_per_page = 25
    save_on_top = True
    
    # Add inline events
    inlines = [ShipmentEventInline]
    
    # Custom actions
    actions = ['mark_in_transit', 'mark_out_for_delivery', 'mark_delivered', 'mark_failed', 'generate_tracking_number']
    
    fieldsets = (
        ('Tracking Info', {
            'fields': ('tracking_number', 'status', 'user', 'tracking_link'),
            'description': 'Core tracking information'
        }),
        ('Sender Information', {
            'fields': ('sender_name', 'sender_email', 'sender_phone'),
            'classes': ('collapse',)
        }),
        ('Receiver Information', {
            'fields': ('receiver_name', 'receiver_email', 'receiver_phone'),
            'classes': ('collapse',)
        }),
        ('Package Details', {
            'fields': ('package_description', 'weight', 'dimensions'),
        }),
        ('Origin Location', {
            'fields': ('origin', ('origin_lat', 'origin_lng')),
            'description': 'Enter coordinates for map display (e.g., New York: 40.7128, -74.0060)'
        }),
        ('Destination Location', {
            'fields': ('destination', ('dest_lat', 'dest_lng')),
        }),
        ('Current Position', {
            'fields': ('current_location', ('current_lat', 'current_lng')),
            'description': 'Update this as the package moves'
        }),
        ('Delivery Schedule', {
            'fields': ('estimated_delivery',),
        }),
        ('System Info', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        """Display status as colored badge"""
        colors = {
            'created': '#6B7280',
            'in_transit': '#3B82F6',
            'out_for_delivery': '#F59E0B',
            'delivered': '#10B981',
            'failed': '#EF4444',
        }
        color = colors.get(obj.status, '#6B7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'
    
    def progress_display(self, obj):
        """Display progress as percentage bar"""
        progress = obj.progress_percentage()
        color = '#10B981' if progress == 100 else '#3B82F6'
        return format_html(
            '<div style="width: 100px; background-color: #E5E7EB; border-radius: 4px; overflow: hidden;">'
            '<div style="width: {}%; background-color: {}; height: 8px;"></div>'
            '</div>'
            '<span style="font-size: 11px; color: #6B7280;">{}%</span>',
            progress, color, int(progress)
        )
    progress_display.short_description = 'Progress'
    
    def tracking_link(self, obj):
        """Generate a clickable tracking link"""
        if obj.tracking_number:
            url = f"/track?tracking={obj.tracking_number}"
            return format_html(
                '<a href="{}" target="_blank" style="color: #3B82F6;">View Tracking Page →</a>',
                url
            )
        return '-'
    tracking_link.short_description = 'Public Link'
    
    # Bulk actions
    @admin.action(description='Mark selected as In Transit')
    def mark_in_transit(self, request, queryset):
        count = queryset.update(status='in_transit')
        self.message_user(request, f'{count} shipment(s) marked as In Transit.')
    
    @admin.action(description='Mark selected as Out for Delivery')
    def mark_out_for_delivery(self, request, queryset):
        count = queryset.update(status='out_for_delivery')
        self.message_user(request, f'{count} shipment(s) marked as Out for Delivery.')
    
    @admin.action(description='Mark selected as Delivered')
    def mark_delivered(self, request, queryset):
        count = queryset.update(status='delivered')
        self.message_user(request, f'{count} shipment(s) marked as Delivered.')
    
    @admin.action(description='Mark selected as Failed')
    def mark_failed(self, request, queryset):
        count = queryset.update(status='failed')
        self.message_user(request, f'{count} shipment(s) marked as Failed.')
    
    @admin.action(description='Generate new tracking numbers')
    def generate_tracking_number(self, request, queryset):
        for shipment in queryset:
            if not shipment.tracking_number or shipment.tracking_number.startswith('TEMP'):
                shipment.tracking_number = f"TTCP{uuid.uuid4().hex[:8].upper()}"
                shipment.save()
        self.message_user(request, f'Tracking numbers generated for selected shipments.')
    
    def save_model(self, request, obj, form, change):
        """Auto-generate tracking number if empty"""
        if not obj.tracking_number:
            obj.tracking_number = f"TTCP{uuid.uuid4().hex[:8].upper()}"
        super().save_model(request, obj, form, change)


@admin.register(ShipmentEvent)
class ShipmentEventAdmin(admin.ModelAdmin):
    list_display = ['shipment_link', 'status_badge', 'location', 'has_coordinates', 'timestamp']
    list_filter = ['status', 'timestamp']
    search_fields = ['shipment__tracking_number', 'status', 'location', 'notes']
    readonly_fields = ['timestamp']
    autocomplete_fields = ['shipment']
    date_hierarchy = 'timestamp'
    list_per_page = 50
    
    fieldsets = (
        ('Event Information', {
            'fields': ('shipment', 'status', 'location'),
        }),
        ('Coordinates (Optional)', {
            'fields': (('latitude', 'longitude'),),
            'description': 'Add coordinates to show this event on the map',
            'classes': ('collapse',)
        }),
        ('Details', {
            'fields': ('notes', 'timestamp'),
        }),
    )
    
    def shipment_link(self, obj):
        """Clickable link to parent shipment"""
        url = reverse('admin:tracking_shipment_change', args=[obj.shipment.id])
        return format_html('<a href="{}">{}</a>', url, obj.shipment.tracking_number)
    shipment_link.short_description = 'Shipment'
    shipment_link.admin_order_field = 'shipment__tracking_number'
    
    def status_badge(self, obj):
        """Display status with color"""
        colors = {
            'created': '#6B7280',
            'picked_up': '#8B5CF6',
            'in_transit': '#3B82F6',
            'at_facility': '#06B6D4',
            'out_for_delivery': '#F59E0B',
            'delivered': '#10B981',
            'failed': '#EF4444',
        }
        color = colors.get(obj.status.lower().replace(' ', '_'), '#6B7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 11px;">{}</span>',
            color,
            obj.status
        )
    status_badge.short_description = 'Status'
    
    def has_coordinates(self, obj):
        """Show if event has map coordinates"""
        if obj.latitude and obj.longitude:
            return format_html('<span style="color: #10B981;">✓ Yes</span>')
        return format_html('<span style="color: #9CA3AF;">✗ No</span>')
    has_coordinates.short_description = 'Map Pin'
