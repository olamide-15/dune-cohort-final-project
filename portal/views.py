from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from functools import wraps
from .forms import AssignmentForm, GradeForm, EnrollmentForm
from .models import AssignmentSubmission,Assignment, Course, Enrollment, Grade

# Create your views here.
def home(request):
    return render(request, 'portal/home.html')

# for custom users

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='login')
        def wrapped(request, *args, **kwargs):
            if request.user.role != role:
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator

#  course crud

@role_required('staff')
def create_course(request):
    if request.method == 'POST':
        title   = request.POST.get('title')
        code    = request.POST.get('code')
        Course.objects.create(
            title=title, code=code, teacher=request.user
        )
        messages.success(request, f'Course "{title}" created.')
        return redirect('staff_dashboard')
    return render(request, 'portal/create_course.html')


@role_required('staff')
def course_detail(request, course_id):
    course      = get_object_or_404(Course, id=course_id)
    enrollments = Enrollment.objects.filter(
        course=course
    ).select_related('student').prefetch_related('grades')
    return render(request, 'portal/course_detail.html', {
        'course':      course,
        'enrollments': enrollments,
    })


@role_required('staff')
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    if request.method == 'POST':
        course.title = request.POST.get('title')
        course.code  = request.POST.get('code')
        course.save()
        messages.success(request, 'Course updated.')
        return redirect('course_detail', course_id=course.id)
    return render(request, 'portal/edit_course.html', {'course': course})


@role_required('staff')
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted.')
        return redirect('staff_dashboard')
    return render(request, 'portal/confirm_delete.html', {'object': course})

#  Assignment Crud

def assignment_create(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Assignment')
    else:
        form = AssignmentForm()
    return render(request, 'portal/create_assignment.html', {'form': form})


@login_required(login_url='login')
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submission = AssignmentSubmission.objects.filter(
        assignment=assignment,
        student=request.user
    ).first()
    return render(request, 'portal/assignment_detail.html', {
        'assignment': assignment,
        'submission': submission,
    })


@role_required('staff')
def assignment_update(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST or None, instance=assignment)
        if form.is_valid():
            form.save()
        messages.success(request, 'Assignment updated.')
        return redirect('course_detail', course_id=assignment.course.id)
    else: 
        form = AssignmentForm(instance=assignment)
    return render(request, 'portal/assignment_update.html', {
        'form': form, 'assignment': assignment
    })

@role_required('staff')
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Assignment deleted.')
        return redirect('course_detail', course_id=assignment.course.id)
    return render(request, 'portal/confirm_delete.html', {'object': assignment})


# Grade 

@role_required('staff')
def add_grade(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    form       = GradeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        grade            = form.save(commit=False)
        grade.enrollment = enrollment
        grade.save()
        messages.success(request, 'Grade recorded.')
        return redirect('course_detail', course_id=enrollment.course.id)
    return render(request, 'portal/add_grade.html', {
        'form': form, 'enrollment': enrollment
    })


@role_required('staff')
def edit_grade(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    form  = GradeForm(request.POST or None, instance=grade)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Grade updated.')
        return redirect('course_detail', course_id=grade.enrollment.course.id)
    return render(request, 'portal/edit_grade.html', {
        'form': form, 'grade': grade
    })

@role_required('staff')
def enroll_student(request):
    form = EnrollmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Student enrolled successfully.')
        return redirect('enrollment_list')
    return render(request, 'portal/enroll_student.html', {'form': form})


@role_required('staff')
def enrollment_list(request):
    enrollments = Enrollment.objects.all().select_related('student', 'course')
    return render(request, 'portal/enrollment_list.html', {
        'enrollments': enrollments
    })


@role_required('staff')
def remove_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Enrollment removed.')
        return redirect('enrollment_list')
    return render(request, 'portal/confirm_delete.html', {'object': enrollment})


# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.utils import timezone
# from functools import wraps
# from .models import (
#     CustomUser, Course, Enrollment,
#     Grade, Assignment, AssignmentSubmission, Announcement
# )
# from .forms import (
#     EditUserForm, GradeForm, AssignmentForm,
#     AnnouncementForm, EnrollmentForm
# )


# # ── Decorator ──────────────────────────────────────────────────────────────────
# def role_required(role):
#     def decorator(view_func):
#         @wraps(view_func)
#         @login_required(login_url='login')
#         def wrapped(request, *args, **kwargs):
#             if request.user.role != role:
#                 return redirect('dashboard')
#             return view_func(request, *args, **kwargs)
#         return wrapped
#     return decorator


# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# # COURSE
# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# @role_required('staff')
# def create_course(request):
#     if request.method == 'POST':
#         title   = request.POST.get('title')
#         code    = request.POST.get('code')
#         Course.objects.create(
#             title=title, code=code, teacher=request.user
#         )
#         messages.success(request, f'Course "{title}" created.')
#         return redirect('staff_dashboard')
#     return render(request, 'portal/create_course.html')


# @role_required('staff')
# def course_detail(request, course_id):
#     course      = get_object_or_404(Course, id=course_id)
#     enrollments = Enrollment.objects.filter(
#         course=course
#     ).select_related('student').prefetch_related('grades')
#     return render(request, 'portal/course_detail.html', {
#         'course':      course,
#         'enrollments': enrollments,
#     })


# @role_required('staff')
# def edit_course(request, course_id):
#     course = get_object_or_404(Course, id=course_id, teacher=request.user)
#     if request.method == 'POST':
#         course.title = request.POST.get('title')
#         course.code  = request.POST.get('code')
#         course.save()
#         messages.success(request, 'Course updated.')
#         return redirect('course_detail', course_id=course.id)
#     return render(request, 'portal/edit_course.html', {'course': course})


# @role_required('staff')
# def delete_course(request, course_id):
#     course = get_object_or_404(Course, id=course_id, teacher=request.user)
#     if request.method == 'POST':
#         course.delete()
#         messages.success(request, 'Course deleted.')
#         return redirect('staff_dashboard')
#     return render(request, 'portal/confirm_delete.html', {'object': course})


# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# # ENROLLMENT
# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# @role_required('staff')
# def enroll_student(request):
#     form = EnrollmentForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         messages.success(request, 'Student enrolled successfully.')
#         return redirect('enrollment_list')
#     return render(request, 'portal/enroll_student.html', {'form': form})


# @role_required('staff')
# def enrollment_list(request):
#     enrollments = Enrollment.objects.all().select_related('student', 'course')
#     return render(request, 'portal/enrollment_list.html', {
#         'enrollments': enrollments
#     })


# @role_required('staff')
# def remove_enrollment(request, enrollment_id):
#     enrollment = get_object_or_404(Enrollment, id=enrollment_id)
#     if request.method == 'POST':
#         enrollment.delete()
#         messages.success(request, 'Enrollment removed.')
#         return redirect('enrollment_list')
#     return render(request, 'portal/confirm_delete.html', {'object': enrollment})


# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# # GRADE
# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# @role_required('staff')
# def add_grade(request, enrollment_id):
#     enrollment = get_object_or_404(Enrollment, id=enrollment_id)
#     form       = GradeForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         grade            = form.save(commit=False)
#         grade.enrollment = enrollment
#         grade.save()
#         messages.success(request, 'Grade recorded.')
#         return redirect('course_detail', course_id=enrollment.course.id)
#     return render(request, 'portal/add_grade.html', {
#         'form': form, 'enrollment': enrollment
#     })


# @role_required('staff')
# def edit_grade(request, grade_id):
#     grade = get_object_or_404(Grade, id=grade_id)
#     form  = GradeForm(request.POST or None, instance=grade)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         messages.success(request, 'Grade updated.')
#         return redirect('course_detail', course_id=grade.enrollment.course.id)
#     return render(request, 'portal/edit_grade.html', {
#         'form': form, 'grade': grade
#     })


# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# # ASSIGNMENT
# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# @role_required('staff')
# def create_assignment(request, course_id):
#     course = get_object_or_404(Course, id=course_id, teacher=request.user)
#     form   = AssignmentForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         assignment        = form.save(commit=False)
#         assignment.course = course
#         assignment.save()
#         messages.success(request, f'Assignment "{assignment.title}" created.')
#         return redirect('course_detail', course_id=course.id)
#     return render(request, 'portal/create_assignment.html', {
#         'form': form, 'course': course
#     })


# @login_required(login_url='login')
# def assignment_detail(request, assignment_id):
#     assignment = get_object_or_404(Assignment, id=assignment_id)
#     submission = AssignmentSubmission.objects.filter(
#         assignment=assignment,
#         student=request.user
#     ).first()
#     return render(request, 'portal/assignment_detail.html', {
#         'assignment': assignment,
#         'submission': submission,
#     })


# @role_required('staff')
# def edit_assignment(request, assignment_id):
#     assignment = get_object_or_404(Assignment, id=assignment_id)
#     form       = AssignmentForm(request.POST or None, instance=assignment)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         messages.success(request, 'Assignment updated.')
#         return redirect('course_detail', course_id=assignment.course.id)
#     return render(request, 'portal/edit_assignment.html', {
#         'form': form, 'assignment': assignment
#     })


# @role_required('staff')
# def delete_assignment(request, assignment_id):
#     assignment = get_object_or_404(Assignment, id=assignment_id)
#     if request.method == 'POST':
#         assignment.delete()
#         messages.success(request, 'Assignment deleted.')
#         return redirect('course_detail', course_id=assignment.course.id)
#     return render(request, 'portal/confirm_delete.html', {'object': assignment})


# @role_required('student')
# def submit_assignment(request, assignment_id):
#     assignment = get_object_or_404(Assignment, id=assignment_id)
#     submission, created = AssignmentSubmission.objects.get_or_create(
#         assignment=assignment,
#         student=request.user
#     )
#     if not submission.submitted:
#         submission.submitted    = True
#         submission.submitted_at = timezone.now()
#         submission.save()
#         messages.success(request, f'"{assignment.title}" submitted.')
#     else:
#         messages.info(request, 'Already submitted.')
#     return redirect('student_dashboard')


# @role_required('staff')
# def view_submissions(request, assignment_id):
#     assignment  = get_object_or_404(Assignment, id=assignment_id)
#     submissions = AssignmentSubmission.objects.filter(
#         assignment=assignment
#     ).select_related('student')
#     return render(request, 'portal/view_submissions.html', {
#         'assignment':  assignment,
#         'submitted':   submissions.filter(submitted=True),
#         'pending':     submissions.filter(submitted=False),
#     })


# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# # ANNOUNCEMENT
# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# @role_required('staff')
# def make_announcement(request):
#     form = AnnouncementForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         announcement            = form.save(commit=False)
#         announcement.created_by = request.user
#         announcement.save()
#         messages.success(request, 'Announcement posted.')
#         return redirect('staff_dashboard')
#     return render(request, 'portal/make_announcement.html', {'form': form})


# @role_required('staff')
# def edit_announcement(request, announcement_id):
#     announcement = get_object_or_404(Announcement, id=announcement_id)
#     form         = AnnouncementForm(request.POST or None, instance=announcement)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         messages.success(request, 'Announcement updated.')
#         return redirect('staff_dashboard')
#     return render(request, 'portal/edit_announcement.html', {
#         'form': form, 'announcement': announcement
#     })


# @role_required('staff')
# def delete_announcement(request, announcement_id):
#     announcement = get_object_or_404(Announcement, id=announcement_id)
#     if request.method == 'POST':
#         announcement.delete()
#         messages.success(request, 'Announcement deleted.')
#         return redirect('staff_dashboard')
#     return render(request, 'portal/confirm_delete.html', {'object': announcement})


# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# # USER MANAGEMENT
# # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# @role_required('staff')
# def edit_user(request, user_id):
#     user = get_object_or_404(CustomUser, id=user_id)
#     form = EditUserForm(
#         request.POST  or None,
#         request.FILES or None,
#         instance=user
#     )
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         messages.success(request, f'{user.get_full_name()} updated.')
#         return redirect('staff_dashboard')
#     return render(request, 'portal/edit_user.html', {
#         'form': form, 'user': user
#     })