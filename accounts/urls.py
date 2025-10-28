from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('doctors/', views.doctors_list, name='doctors_list'),
    path('patients/', views.patients_list, name='patients_list'),
    path('doctor/<int:pk>/', views.doctor_profile, name='doctor_profile'),
    path('patient/<int:pk>/', views.patient_profile, name='patient_profile'),
]


