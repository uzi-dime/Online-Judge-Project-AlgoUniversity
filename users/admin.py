# users/admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

# Get the custom model
User = get_user_model()

# Unregister any existing registration for this model (e.g., auth.UserAdmin)
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class CustomUserAdmin(DefaultUserAdmin):
    """
    Custom admin for the custom User model.
    Inherits from Django's default UserAdmin but adds and reorders fields
    to expose custom profile attributes.
    """
    # Columns displayed in the user list view
    list_display = (
        'username',
        'email',
        'problems_solved',
        'rating',
        'skill_level',
        'is_staff',
        'is_active',
    )
    # Filters available in the sidebar
    list_filter = (
        'skill_level',
        'is_staff',
        'is_superuser',
        'is_active',
        'groups',
    )
    # Ordering default for the changelist view
    ordering = ('-rating',)

    # Fieldsets control grouping of fields on the user edit page
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'bio',
                'avatar',
                'institution',
                'country',
            )
        }),
        ('Social links', {
            'fields': (
                'github_profile',
                'linkedin_profile',
                'website',
            )
        }),
        ('Programming stats', {
            'fields': (
                'preferred_languages',
                'skill_level',
                'problems_solved',
                'total_submissions',
                'successful_submissions',
                'rating',
                'contests_participated',
            )
        }),
        ('Achievements & points', {
            'fields': (
                'badges',
                'experience_points',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # Fields shown when creating a new user via admin “Add user” form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
                'skill_level',
            ),
        }),
    )

    # Enable searching by these fields
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'institution',
    )
