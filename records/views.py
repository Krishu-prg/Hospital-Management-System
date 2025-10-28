from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import doctor_required, patient_required
from .models import MedicalRecord, Report
from .forms import MedicalRecordForm, ReportForm


@login_required
def list_records(request):
    if request.user.is_doctor():
        qs = MedicalRecord.objects.select_related('patient', 'doctor')
    else:
        qs = MedicalRecord.objects.filter(patient=request.user)
    return render(request, 'records/list.html', { 'records': qs[:200] })


@doctor_required
def create_record(request, patient_id):
    from accounts.models import User
    patient = get_object_or_404(User, pk=patient_id)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            rec = form.save(commit=False)
            rec.patient = patient
            rec.doctor = request.user
            rec.save()
            messages.success(request, 'Record created.')
            return redirect('records:list')
    else:
        form = MedicalRecordForm()
    return render(request, 'records/form.html', { 'form': form, 'patient': patient })


@doctor_required
def add_report(request, record_id):
    rec = get_object_or_404(MedicalRecord, pk=record_id)
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            rpt = form.save(commit=False)
            rpt.record = rec
            rpt.save()
            messages.success(request, 'Report uploaded.')
            return redirect('records:list')
    else:
        form = ReportForm()
    return render(request, 'records/report_form.html', { 'form': form, 'record': rec })

# Create your views here.
