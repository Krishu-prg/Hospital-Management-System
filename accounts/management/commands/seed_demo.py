from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random

from accounts.models import User, DoctorProfile, PatientProfile
from appointments.models import Department, Appointment


class Command(BaseCommand):
    help = 'Seed demo data: departments, doctors, patients, appointments'

    def handle(self, *args, **options):
        fake = Faker()

        # Departments
        dept_names = ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'Dermatology']
        depts = []
        for name in dept_names:
            d, _ = Department.objects.get_or_create(name=name)
            depts.append(d)

        # Doctors
        doctors = []
        for i in range(6):
            u, created = User.objects.get_or_create(username=f'doctor{i+1}', defaults={
                'first_name': fake.first_name(), 'last_name': fake.last_name(), 'email': fake.email(), 'role': 'DOCTOR'
            })
            if created:
                u.set_password('pass12345')
                u.save()
            DoctorProfile.objects.get_or_create(user=u, defaults={'specialization': random.choice(dept_names), 'phone': fake.phone_number(), 'room_number': str(100+i)})
            doctors.append(u)

        # Patients
        patients = []
        for i in range(20):
            u, created = User.objects.get_or_create(username=f'patient{i+1}', defaults={
                'first_name': fake.first_name(), 'last_name': fake.last_name(), 'email': fake.email(), 'role': 'PATIENT'
            })
            if created:
                u.set_password('pass12345')
                u.save()
            PatientProfile.objects.get_or_create(user=u, defaults={'gender': random.choice(['M','F','O']), 'phone': fake.phone_number(), 'address': fake.address()})
            patients.append(u)

        # Appointments
        for p in patients:
            for _ in range(random.randint(1,3)):
                d = random.choice(doctors)
                dept = random.choice(depts)
                day = timezone.localdate() + timezone.timedelta(days=random.randint(-30, 30))
                time = timezone.datetime.now().time().replace(hour=random.randint(9,16), minute=random.choice([0,30]), second=0, microsecond=0)
                status = random.choice([Appointment.Status.PENDING, Appointment.Status.APPROVED, Appointment.Status.COMPLETED])
                try:
                    Appointment.objects.create(patient=p, doctor=d, department=dept, date=day, time=time, status=status)
                except Exception:
                    pass

        self.stdout.write(self.style.SUCCESS('Demo data seeded.'))


