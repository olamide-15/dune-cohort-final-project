from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Announcement, Course, Assignment,Enrollment, AssignmentSubmission, Grade

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'get_full_name', 'email', 'role', 'is_active']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    fieldsets = UserAdmin.fieldsets + (
        ('Portal info', {'fields': ('role', 'phone', 'class_name', 'children')}),
    )

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'teacher']
    search_fields = ['code', 'title']
    list_filter =['teacher']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display  = ['student', 'course', 'date']
    search_fields = ['student__first_name', 'student__last_name', 'course__title']
    list_filter   = ['course', 'date']

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display  = ('get_student', 'get_course', 'term', 'score', 'recorded_at')
    search_fields = ('enrollment__student__first_name', 'enrollment__course__title')
    list_filter   = ('term',)

    # custom column — pulls student name from the enrollment
    def get_student(self, obj):
        return obj.enrollment.student.get_full_name()
    get_student.short_description = 'Student'  # column header name

    # custom column — pulls course title from the enrollment
    def get_course(self, obj):
        return obj.enrollment.course.title
    get_course.short_description = 'Course'


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display  = ('title', 'course', 'due_date')
    search_fields = ('title', 'course__title')
    list_filter   = ('course', 'due_date') 

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display  = ('student', 'assignment', 'submitted', 'submitted_at')
    search_fields = ('student__first_name', 'assignment__title')
    list_filter   = ('submitted',)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display  = ('title', 'audience', 'created_by', 'created_at')
    search_fields = ('title', 'body')
    list_filter   = ('audience',)