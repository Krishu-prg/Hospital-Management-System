from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.list_appointments, name='list'),
    path('book/', views.book_appointment, name='book'),
    path('<int:pk>/approve/', views.approve_appointment, name='approve'),
    path('<int:pk>/reject/', views.reject_appointment, name='reject'),
    path('<int:pk>/complete/', views.complete_appointment, name='complete'),
]


