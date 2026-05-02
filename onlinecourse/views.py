from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Question, Submission, Enrollment

def submit(request, course_id):
    """
    Handles the exam submission by collecting selected choices 
    and creating a submission record.
    """
    course = get_object_or_404(Course, pk=course_id)
    # Get enrollment for the current user
    enrollment = Enrollment.objects.get(user=request.user, course=course)
    
    if request.method == 'POST':
        # Retrieve all selected choice IDs from the form
        selected_ids = request.POST.getlist('choice')
        # Create a new submission object
        submission = Submission.objects.create(enrollment=enrollment)
        # Link selected choices to the submission
        for choice_id in selected_ids:
            submission.choices.add(choice_id)
        
        return redirect('onlinecourse:show_exam_result', 
                        course_id=course.id, 
                        submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    """
    Calculates the score based on correct choices and displays the result.
    """
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    total_score = 0
    
    # Get all questions related to this course
    questions = Question.objects.filter(lesson__course=course)
    # Get the IDs of the choices the user selected
    selected_ids = submission.choices.values_list('id', flat=True)
    
    for question in questions:
        # Check if the selection for this specific question is correct
        if question.is_get_score(selected_ids):
            total_score += question.grade
            
    return render(request, 'onlinecourse/exam_result.html', {
        'course': course, 
        'score': total_score,
        'submission': submission
    })
