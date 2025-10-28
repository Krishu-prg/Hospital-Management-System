from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User, DoctorProfile, PatientProfile


@login_required
def doctors_list(request):
    doctors = User.objects.filter(role=User.Roles.DOCTOR).select_related('doctor_profile')
    return render(request, 'accounts/doctors_list.html', { 'doctors': doctors })


@login_required
def patients_list(request):
    patients = User.objects.filter(role=User.Roles.PATIENT).select_related('patient_profile')
    return render(request, 'accounts/patients_list.html', { 'patients': patients })


@login_required
def doctor_profile(request, pk):
    user = get_object_or_404(User, pk=pk, role=User.Roles.DOCTOR)
    return render(request, 'accounts/doctor_profile.html', { 'doctor': user })


@login_required
def patient_profile(request, pk):
    user = get_object_or_404(User, pk=pk, role=User.Roles.PATIENT)
    return render(request, 'accounts/patient_profile.html', { 'patient': user })

# Create your views here.
