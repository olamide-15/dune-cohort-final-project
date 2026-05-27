from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from functools import wraps
from .forms import RegistrationForm
# from .decorators import role_required
from portal.models import Enrollment, Grade, AssignmentSubmission, Announcement


# Create your views here.

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
    role_map = {
        'student': 'student_dashboard',
        'parent': 'parent_dashboard',
        'staff': 'staff_dashboard',
    }
    destination = role_map.get(request.user.role)
    if destination:
        return redirect(destination)
    return redirect('login')

@role_required('student')
def student_dashboard(request):
    student = request.user
    enrollments = Enrollment.objects.filter(
        student=student 
    ).select_related('course')

    grades = Grade.objects.filter(enrollment__student=student).select_related('enrollment__course')

    scores = [g.scores for g in grades]
    average = round(sum(scores) / len(scores), 1) if scores else None

    submissions = AssignmentSubmission.objects.filter(
        student=student
    ).select_related('assignment', 'assignment__course')

    announcements = Announcement.objects.filter(
        audience__in=['all', 'student']
    ).order_by('created_at')[:5]

    return render(request, 'account/student_dashboard.html', {
        'student':       student,
        'enrollments':   enrollments,
        'grades':        grades,
        'average':       average,
        'submissions':   submissions,
        'announcements': announcements,
    })


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
    from portal.models import Course

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