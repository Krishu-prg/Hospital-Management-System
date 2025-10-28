from django.contrib import admin
from .models import Department, Appointment


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "department", "date", "time", "status")
    list_filter = ("status", "department", "date")
    search_fields = ("patient__username", "doctor__username")

# Register your models here.
