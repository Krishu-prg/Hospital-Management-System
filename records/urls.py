from django.urls import path
from . import views

app_name = 'records'

urlpatterns = [
    path('', views.list_records, name='list'),
    path('create/<int:patient_id>/', views.create_record, name='create'),
    path('<int:record_id>/report/', views.add_report, name='add_report'),
]


