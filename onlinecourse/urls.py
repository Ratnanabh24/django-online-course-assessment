from django.urls import path
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # Task 6: Path for submitting the exam
    path('course/<int:course_id>/submit/', views.submit, name='submit'),
    # Task 6: Path for showing the exam result
    path('course/<int:course_id>/submission/<int:submission_id>/result/', 
         views.show_exam_result, name='show_exam_result'),
]
