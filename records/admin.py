from django.contrib import admin
from .models import MedicalRecord, Report


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "created_at")
    search_fields = ("patient__username", "doctor__username")


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("record", "title", "created_at")

# Register your models here.
