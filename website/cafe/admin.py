from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage, JobApplication, Coffee


# ----------------------------
# CONTACT MESSAGES (Read Only)
# ----------------------------
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email", "message")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

    readonly_fields = ("name", "email", "message", "created_at")
    fields = ("name", "email", "message", "created_at")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True


# ----------------------------
# JOB APPLICATIONS (Read Only + Badge Status + Actions)
# ----------------------------
@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "position", "colored_status", "created_at")
    list_filter = ("position", "status", "created_at")
    search_fields = ("full_name", "email", "phone", "message")
    ordering = ("-created_at",)

    readonly_fields = (
        "full_name",
        "email",
        "phone",
        "position",
        "message",
        "cv",
        "status",
        "created_at",
    )

    fields = (
        "full_name",
        "email",
        "phone",
        "position",
        "message",
        "cv",
        "status",
        "created_at",
    )

    # Actions për status (dinamikisht)
    actions = ("mark_reviewed", "mark_accepted", "mark_rejected")

    @admin.action(description="Mark selected applications as Reviewed")
    def mark_reviewed(self, request, queryset):
        queryset.update(status="reviewed")

    @admin.action(description="Mark selected applications as Accepted")
    def mark_accepted(self, request, queryset):
        queryset.update(status="accepted")

    @admin.action(description="Mark selected applications as Rejected")
    def mark_rejected(self, request, queryset):
        queryset.update(status="rejected")

    # Badge me ngjyra për status
    def colored_status(self, obj):
        color_map = {
            "pending": "#6c757d",     # grey
            "reviewed": "#0d6efd",    # blue
            "accepted": "#198754",    # green
            "rejected": "#dc3545",    # red
        }
        color = color_map.get(obj.status, "#000")

        return format_html(
            '<span style="color:white; background-color:{}; padding:4px 10px; border-radius:12px; font-size:12px;">{}</span>',
            color,
            obj.get_status_display()
        )

    colored_status.short_description = "Status"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

@admin.register(Coffee)
class CoffeeAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available")
    list_filter = ("category", "is_available")
    search_fields = ("name",)
