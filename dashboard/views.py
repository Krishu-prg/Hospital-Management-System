from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.utils import timezone

from accounts.models import User
from appointments.models import Appointment


@login_required
def home(request):
    user: User = request.user
    if user.is_superuser or user.is_admin():
        return redirect('dashboard:admin')
    if user.is_doctor():
        return redirect('dashboard:doctor')
    return redirect('dashboard:patient')


@login_required
def admin_dashboard(request):
    total_doctors = User.objects.filter(role=User.Roles.DOCTOR).count()
    total_patients = User.objects.filter(role=User.Roles.PATIENT).count()
    total_appointments = Appointment.objects.count()

    latest_appointments = Appointment.objects.select_related('patient', 'doctor').order_by('-created_at')[:10]

    context = {
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'latest_appointments': latest_appointments,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
def admin_appointments_per_month(request):
    # Simple stub data; can be replaced by real aggregation
    data = {"labels": ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
            "values": [12,9,14,20,18,10,25,30,22,19,15,17]}
    return JsonResponse(data)


@login_required
def doctor_dashboard(request):
    today = timezone.localdate()
    todays_appointments = Appointment.objects.filter(doctor=request.user, date=today).select_related('patient')
    context = {
        'todays_appointments': todays_appointments,
    }
    return render(request, 'dashboard/doctor_dashboard.html', context)


@login_required
def patient_dashboard(request):
    upcoming = Appointment.objects.filter(patient=request.user, date__gte=timezone.localdate()).order_by('date', 'time')
    past = Appointment.objects.filter(patient=request.user, date__lt=timezone.localdate()).order_by('-date', '-time')[:10]
    context = {
        'upcoming': upcoming,
        'past': past,
    }
    return render(request, 'dashboard/patient_dashboard.html', context)

# Create your views here.
