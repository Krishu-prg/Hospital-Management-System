from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        DOCTOR = "DOCTOR", _("Doctor")
        PATIENT = "PATIENT", _("Patient")

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.PATIENT,
        help_text=_("Determines the user dashboard and permissions."),
    )

    def is_admin(self) -> bool:
        return self.role == self.Roles.ADMIN or self.is_superuser

    def is_doctor(self) -> bool:
        return self.role == self.Roles.DOCTOR

    def is_patient(self) -> bool:
        return self.role == self.Roles.PATIENT


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    specialization = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    room_number = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        return f"Dr. {self.user.get_full_name() or self.user.username}"


class PatientProfile(models.Model):
    GENDER_CHOICES = (
        ("M", _("Male")),
        ("F", _("Female")),
        ("O", _("Other")),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        return self.user.get_full_name() or self.user.username

# Create your models here.
