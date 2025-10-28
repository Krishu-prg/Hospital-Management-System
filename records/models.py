from django.db import models
from django.conf import settings
from django.utils import timezone


class MedicalRecord(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="medical_records")
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="authored_records")
    appointment = models.ForeignKey('appointments.Appointment', on_delete=models.SET_NULL, null=True, blank=True)
    diagnosis = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"Record for {self.patient} at {self.created_at:%Y-%m-%d}"


class Report(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name="reports")
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="reports/")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.title

# Create your models here.
