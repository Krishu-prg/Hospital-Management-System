from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from accounts.decorators import admin_required, doctor_required, patient_required
from accounts.models import User
from .models import Appointment, Department
from .forms import AppointmentForm


@login_required
def list_appointments(request):
    qs = Appointment.objects.select_related('patient', 'doctor', 'department')
    user: User = request.user
    if user.is_doctor():
        qs = qs.filter(doctor=user)
    elif user.is_patient():
        qs = qs.filter(patient=user)
    query = request.GET.get('q')
    if query:
        qs = qs.filter(Q(patient__username__icontains=query) | Q(doctor__username__icontains=query))
    return render(request, 'appointments/list.html', { 'appointments': qs[:200], 'departments': Department.objects.all() })


@patient_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt: Appointment = form.save(commit=False)
            appt.patient = request.user
            appt.status = Appointment.Status.PENDING
            # Prevent double booking by unique_together
            try:
                appt.save()
                messages.success(request, 'Appointment requested, pending approval.')
                return redirect('appointments:list')
            except Exception:
                form.add_error(None, 'Selected doctor/time slot is not available.')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/book.html', { 'form': form })


@admin_required
def approve_appointment(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    appt.status = Appointment.Status.APPROVED
    appt.save(update_fields=['status'])
    messages.success(request, 'Appointment approved.')
    return redirect('appointments:list')


@admin_required
def reject_appointment(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    appt.status = Appointment.Status.REJECTED
    appt.save(update_fields=['status'])
    messages.info(request, 'Appointment rejected.')
    return redirect('appointments:list')


@doctor_required
def complete_appointment(request, pk):
    appt = get_object_or_404(Appointment, pk=pk, doctor=request.user)
    appt.status = Appointment.Status.COMPLETED
    appt.save(update_fields=['status'])
    messages.success(request, 'Marked as completed.')
    return redirect('appointments:list')

# Create your views here.
