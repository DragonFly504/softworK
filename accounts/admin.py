from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile - shows profile fields on User edit page"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile Details'
    fk_name = 'user'
    fieldsets = (
        ('Personal Information', {
            'fields': ('phone', 'date_of_birth', 'ssn')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'zipcode', 'country')
        }),
    )


class UserAdmin(BaseUserAdmin):
    """Extended User admin with profile inline"""
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone')
    list_select_related = ('profile',)
    
    def get_phone(self, instance):
        try:
            return instance.profile.phone
        except UserProfile.DoesNotExist:
            return '-'
    get_phone.short_description = 'Phone'
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Standalone UserProfile admin"""
    list_display = ('user', 'phone', 'city', 'state', 'country', 'created_at')
    list_filter = ('country', 'state', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'city')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('phone', 'date_of_birth', 'ssn')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'zipcode', 'country')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Re-register UserAdmin with profile inline
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
