from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from django.utils import timezone 
from portal.models import CustomUser, Enrollment, Grade, AssignmentSubmission, Announcement, Course
from portal.forms import AssignmentForm, GradeForm, AnnouncementForm, CourseForm
from portal.forms import CourseForm, GradeForm, AnnouncementForm, SubmissionForm, AdminEnrollmentForm, AdminAddStudentForm


# Create your views here.

def role_required(role):
    def decorator(view_func):
        @login_required(login_url='login')
        def wrapped(request, *args, **kwargs):
            if request.user.role != role:
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect("dashboard")  
    else:
        form = RegistrationForm()
    return render(request, "account/register.html", {"form": form})


@login_required(login_url='login')
def dashboard(request):
    destinations = {
        'student': 'student_dashboard',
        'parent': 'parent_dashboard',
        'staff': 'staff_dashboard',
        'admin': 'admin_dashboard',
    }
    target = destinations.get(request.user.role)
    return redirect(target) if target else redirect('login')

@role_required('student')
def student_dashboard(request):
    student = request.user
    enrollments = Enrollment.objects.filter(
        student=student 
    ).select_related('course')

    grades = Grade.objects.filter(enrollment__student=student).select_related('enrollment__course')

    scores = [g.score for g in grades]
    average = round(sum(scores) / len(scores), 1) if scores else None

    submissions = AssignmentSubmission.objects.filter(
        student=student
    ).select_related('assignment', 'assignment__course')

    announcements = Announcement.objects.filter(
        audience__in=['all', 'student']
    ).order_by('-created_at')[:5]

    return render(request, 'account/student_dashboard.html', {
        'student':       student,
        'enrollments':   enrollments,
        'grades':        grades,
        'average':       average,
        'submissions':   submissions,
        'announcements': announcements,
    })

@login_required(login_url='login')
def student_courses(request):
    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related('course')
    context = {'enrollments': enrollments}
    return render(request, 'account/student_courses.html', context)

@login_required(login_url='login')
def student_assignments(request):
    today = timezone.now().date()
    submissions = AssignmentSubmission.objects.filter(
        student=request.user
    ).select_related('assignment__course').order_by('assignment__due_date')
      
    for sub in submissions:
        if sub.submitted:
            sub.status = 'submitted'
        elif sub.assignment.due_date < today:
            sub.status ='Overdue'
        elif sub.assignment.due_date <=today + timezone.timedelta(days=3):
            sub.status = 'due_soon'
        else:
            sub.status = 'pending'
    
    context = {'submissions': submissions,
               'today': today,}
    return render(request, 'account/student_assignments.html', context)


@login_required(login_url='login')
def student_submit_assignment(request, submission_id):
    submission = get_object_or_404(
        AssignmentSubmission.objects.select_related(
        'assignment')
    ).get(id=submission_id, student=request.user)

    if submission.submitted:
        return redirect('student_assignments')
    if submission.assignment.due_date < timezone.now().date():
        return redirect('student_assignments')

    form = SubmissionForm(request.POST or None, request.FILES or None, instance=submission)
    if form.is_valid():
        sub = form.save(commit=False)
        sub.submitted = True
        sub.submitted_at = timezone.now()
        sub.save()
        return redirect('student_assignments')

    return render(request, 'account/student_submit.html', {
        'form': form,
        'submission': submission,
    })

@login_required(login_url='login')
def student_profile(request):
    context = {'student': request.user}
    return render(request, 'account/student_profile.html', context)


@role_required('parent')
def parent_dashboard(request):
    children      = request.user.children.filter(role='student')
    children_data = []

    for child in children:
        grades  = Grade.objects.filter(
            enrollment__student=child
        ).select_related('enrollment__course')

        scores  = [g.score for g in grades]
        average = round(sum(scores) / len(scores), 1) if scores else None

        submissions = AssignmentSubmission.objects.filter(
            student=child
        ).select_related('assignment', 'assignment__course')

        children_data.append({
            'child':       child,
            'grades':      grades,
            'average':     average,
            'submissions': submissions,
            'pending':     submissions.filter(submitted=False).count(),
        })

    announcements = Announcement.objects.filter(
        audience__in=['all', 'parent']
    ).order_by('-created_at')[:5]

    return render(request, 'account/parent_dashboard.html', {
        'children_data': children_data,
        'announcements': announcements,
        'has_children':  children.exists(),
    })

@role_required('staff')
def staff_dashboard(request):
   
    teacher = request.user
    courses = Course.objects.filter(
        teacher=teacher
    ).prefetch_related('enrollments', 'assignments')

    pending_submissions = AssignmentSubmission.objects.filter(
        assignment__course__teacher=teacher,
        submitted=True
    ).select_related('student', 'assignment', 'assignment__course')

    announcements = Announcement.objects.filter(
        audience__in=['all', 'staff']
    ).order_by('-created_at')[:5]

    return render(request, 'account/staff_dashboard.html', {
        'teacher':             teacher,
        'courses':             courses,
        'pending_submissions': pending_submissions,
        'announcements':       announcements,
    })

@login_required
def staff_student_profiles(request):
    students = CustomUser.objects.filter(
        role='student'
    ).order_by('last_name', 'first_name')

    return render(request, 'account/staff_student_profiles.html', {
        'students': students,
    })

@role_required('staff')
def staff_add_course(request):
    form = CourseForm(request.POST or None)
    if form.is_valid():
        course = form.save(commit=False)
        course.teacher = request.user
        course.save()
        return redirect('staff_dashboard')
    return render(request, 'account/staff_add_course.html', {'form': form})


@role_required('staff')
def staff_add_grade(request):
    form = GradeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('staff_dashboard')
    return render(request, 'account/staff_add_grade.html', {'form': form})



@role_required('staff')
def staff_view_submissions(request):
    submissions = AssignmentSubmission.objects.filter(
        assignment__course__teacher=request.user
    ).select_related('student', 'assignment__course').order_by('-submitted_at')

    return render(request, 'account/staff_view_submission.html', {
        'submissions': submissions,
    })

@role_required('staff')
def staff_add_announcement(request):
    form = AnnouncementForm(request.POST or None)
    if form.is_valid():
        announcement = form.save(commit=False)
        announcement.created_by = request.user
        announcement.save()
        return redirect('staff_dashboard')
    return render(request, 'account/staff_add_announcement.html', {'form': form})

@role_required('admin')
def admin_dashboard(request):
    total_students   = CustomUser.objects.filter(role='student').count()
    total_courses    = Course.objects.count()
    total_enrollments = Enrollment.objects.count()

    return render(request, 'account/admin_dashboard.html', {
        'total_students':    total_students,
        'total_courses':     total_courses,
        'total_enrollments': total_enrollments,
    })

@role_required('admin')
def admin_enrollments(request):
    enrollments = Enrollment.objects.select_related(
        'student', 'course'
    ).order_by('course__title', 'student__last_name')

    return render(request, 'account/admin_enrollments.html', {
        'enrollments': enrollments,
    })

@role_required('admin')
def admin_enroll_student(request):
    form = AdminEnrollmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('admin_enrollments')
    return render(request, 'account/admin_enroll_student.html', {
        'form': form,
    })

@role_required('admin')
def admin_remove_enrollment(request, enrollment_id):
    try:
        enrollment = Enrollment.objects.select_related(
            'student', 'course'
        ).get(id=enrollment_id)
    except Enrollment.DoesNotExist:
        return redirect('admin_enrollments')

    if request.method == 'POST':
        enrollment.delete()
        return redirect('admin_enrollments')

    return render(request, 'account/admin_confirm_remove.html', {
        'enrollment': enrollment,
    })

@role_required('admin')
def admin_add_student(request):
    form = AdminAddStudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('admin_dashboard')
    return render(request, 'account/admin_add_student.html', {'form': form})

