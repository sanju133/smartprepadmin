from django.urls import path
from lecturer import views

urlpatterns = [
    path('lecturerDashboard/', views.lecturer_dashboard),
    path('course_form/', views.courses_form),
    path('get_course/', views.get_course),
    path('course_update_form/<int:courses_id>', views.course_update_form),

    # path('lecture_form/', views.lectures_form),
    path('get_lecture/', views.get_lecture),

    path('delete_course/<int:courses_id>', views.delete_course),

    # path('lecture_update_form/<int:lectures_id>', views.lecture_update_form),

    path('lecture_form/', views.lectures_form),
    path('get_lecture/', views.get_lecture),
    path('get_particular_lecture/<int:courses_id>', views.get_particular_lecture),
    path('lecture_update_form/<int:lectures_id>', views.lecture_update_form),
    path('delete_lecture/<int:lectures_id>', views.delete_lecture),

]

