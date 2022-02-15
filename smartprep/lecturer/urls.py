from django.urls import path
from lecturer import views

urlpatterns = [
    path('lecturerDashboard/', views.lecturer_dashboard),
    path('course_form/', views.courses_form),
    path('get_course/', views.get_course),
    path('lecture_form/', views.lectures_form),
    path('get_lecture/', views.get_lecture),



]

