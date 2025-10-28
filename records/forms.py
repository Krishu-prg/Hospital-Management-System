from django import forms
from .models import MedicalRecord, Report


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ["appointment", "diagnosis", "prescription", "notes"]
        widgets = {
            "diagnosis": forms.Textarea(attrs={"rows": 2}),
            "prescription": forms.Textarea(attrs={"rows": 2}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["title", "file"]


