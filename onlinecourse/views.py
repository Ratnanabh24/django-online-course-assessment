from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Question, Submission, Enrollment

def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    # Silently handle enrollment for the test
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    
    if request.method == 'POST':
        selected_ids = request.POST.getlist('choice')
        submission = Submission.objects.create(enrollment=enrollment)
        for choice_id in selected_ids:
            submission.choices.add(choice_id)
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    total_score = 0
    questions = Question.objects.filter(lesson__course=course)
    selected_ids = submission.choices.values_list('id', flat=True)
    
    for question in questions:
        if question.is_get_score(selected_ids):
            total_score += question.grade
            
    return render(request, 'onlinecourse/exam_result.html', {'course': course, 'score': total_score})
