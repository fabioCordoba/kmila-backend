from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.users.models.user import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "rol", "is_active", "is_staff", "is_superuser")
    list_filter = ("rol", "is_staff", "is_superuser", "is_active")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "image", "rol")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "rol",
                    "image",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    search_fields = ("username", "email")
    ordering = ("username",)
