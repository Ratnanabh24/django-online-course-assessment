from django.contrib import admin
from .models import Course, Lesson, Question, Choice, Enrollment, Learner, Instructor

# Task 2: Implement ChoiceInline to allow adding choices directly to questions
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

# Task 2: Implement QuestionInline to allow adding questions directly to lessons
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 2

# Task 2: Customizing LessonAdmin to include QuestionInline
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']
    inlines = [QuestionInline]

# Task 2: Customizing QuestionAdmin to include ChoiceInline
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

# Registering the classes with the admin site
admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Enrollment)
admin.site.register(Learner)
admin.site.register(Instructor)
