*{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body{
    display: flex;
    flex-direction: row;
}

nav{
    width: 30%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: rgb(8, 8, 117);
}


.logo img {
  max-width: 130px;
  height: auto;
  display: block;
}

.navRight{
    display: flex;
    gap: 20px;
}

.navRight a{
    text-decoration: none;
    color: #fff;
    /* border: 2px solid red; */
    background-color: rgb(19, 19, 183);
    padding: 5px 10px;
    border-radius: 10px;
    cursor: pointer;
}

main{
    height: 82vh;
    width: 70%;
    background-image: url("{% static 'image/nick-morrison-FHnnjk1Yj7Y-unsplash.jpg' %}");
}

footer{
    background-color: rgb(8, 8, 117);
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
}

footer p{
    color: #fff;
}




<nav>
              

         <a href="/" class="logo">
        {% comment %} <img src="{% static 'image/logo.png' %}" alt="smartstudy Logo"> {% endcomment %}
        </a> 
        <div class="navRight">
            <a href="/">Dashboard</a>
            <a href="/students/">student</a>
            <a href="/about/">About</a>
            <a href="/courses/">course</a>
        </div>
        <a href="{% url 'login' %}">Login</a>
        <a href="{% url 'register' %}">Register</a>
    </nav>

    <main>

        {% if messages %}
            {% for messages in messages %}
                <div class='alert alert-{{ message.tags }}'>
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}

        {% block content%}
        {% endblock %}















        {% load static %}

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %} SmartStudy {% endblock %}</title>
    <link rel='stylesheet' href="{% static 'css/main.css' %}"> 

</head>
<body>
    <script  src="{% static 'js/main.js' %}"></script>

    <nav>

        <a href="/" class="logo"><img src="{% static 'image/logo.png' %}" alt="smartstudy Logo"> </a> 
            <h2>SmartStudy</h2>
                  
            <div class="nav-links">
            <a href="/">Home</a>
    

            {% if request.user.is_authenticated and request.user.is_student %}
            <!-- show only to logged-in users -->

                <span style="color: white; padding: 8px 16px;">Hello, {{ request.user.username }}</span>

                <!-- Corrected logout: Must use POST for Django 5.0+ -->
                <form action="{% url 'logout' %}" method="post" style="display: inline;">
                {% csrf_token %}
                <button type="submit">Logout</button>
                </form>

                <form action="{% url 'logout' %}" method="post" style="display: inline;">
                    {% csrf_token %}
                    <button type="submit">Logout</button>
                </form>
            {% elif request.user.is_authenticated and request.user.is_staff_member %}    
                <a href="{% url 'staff_dashboard' %}">🏠 Dashboard</a>
            {% comment %} <a href="{% url 'staff_student_profiles' %}">👥 Student Profiles</a> {% endcomment %}
            {% comment %} <a href="{% url 'staff_add_course' %}">📚 Add Course</a> {% endcomment %}
            {% comment %} <a href="{% url 'staff_add_grade' %}">🎓 Add Grade</a> {% endcomment %}
            {% comment %} <a href="{% url 'staff_view_submissions' %}">📝 View Submissions</a> {% endcomment %}
            {% comment %} <a href="{% url 'staff_add_announcement' %}">📢 Add Announcement</a> {% endcomment %}
                <span style="color: white; padding: 8px 16px;">Hello, {{ request.user.username }}</span>


                <form method="post" action="{% url 'logout' %}" style="display:inline;">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-link" style="padding:0; margin:0; border:none; background:none;">
                        Logout
                    </button>
                </form>

            {% else %}
                <!-- Shown only to loggged-out visitors -->
                <a href="{% url 'login' %}">Login</a>
                <a href="{% url 'register' %}">Register</a>
            {% endif %}
        </div>         
    </nav>



        
        <!-- Sidebar: visible to students and staff -->


    <nav class="sidebar-nav">
        {% if request.user.is_student %}
            <a href="{% url 'student_dashboard' %}">🏠 Dashboard</a>
            <a href="{% url 'student_courses' %}">📚 Courses</a>
            <a href="{% url 'student_assignments' %}">📝 Assignments</a>
            <a href="{% url 'student_profile' %}">👤 Profile</a>
{% comment %} 
        {% elif request.user.is_staff_member %}
            <a href="{% url 'staff_dashboard' %}">🏠 Dashboard</a> {% endcomment %}
            {% comment %} <a href="{% url 'staff_student_profiles' %}">👥 Student Profiles</a> {% endcomment %}
            {% comment %} <a href="{% url 'staff_add_course' %}">📚 Add Course</a> {% endcomment %}
            {% comment %} <a href="{% url 'staff_add_grade' %}">🎓 Add Grade</a> {% endcomment %}
            {% comment %} <a href="{% url 'staff_view_submissions' %}">📝 View Submissions</a> {% endcomment %}
            {% comment %} <a href="{% url 'staff_add_announcement' %}">📢 Add Announcement</a> {% endcomment %}
        {% comment %} {% endif %} {% endcomment %}
    </nav>

{% endif %}


    <main>

        {% if messages %}
            {% for message in messages %}
                <div class='alert alert-{{ message.tags }}'>
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}

        {% block content%}
        {% endblock %}
        <footer>
            <p>copyright &copy; smartstudy</p>
        </footer>
    </main>
    
    
    
</body>


</html>





<!-- view.py -->
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



<!-- urls.py  -->
# path('assignment/<int:assignment_id>/submit/',   views.submit_assignment, name='submit_assignment'),
    # path('assignment/<int:assignment_id>/submissions/', views.view_submissions, name='view_submissions'),

    # "token": "e0878ea76a0f640cf390877f4fb82c585bcf584a"


    # ── Course ────────────────────────────────────────────────────────────────
    # path('course/create/',              views.create_course,    name='create_course'),
    # path('course/<int:course_id>/',     views.course_detail,    name='course_detail'),
    # path('course/<int:course_id>/edit/',views.edit_course,      name='edit_course'),
    # path('course/<int:course_id>/delete/',views.delete_course,  name='delete_course'),

    # # ── Enrollment ────────────────────────────────────────────────────────────
    # path('enrollment/',                     views.enrollment_list,    name='enrollment_list'),
    # path('enrollment/add/',                 views.enroll_student,     name='enroll_student'),
    # path('enrollment/<int:enrollment_id>/delete/', views.remove_enrollment, name='remove_enrollment'),

    # # ── Grade ─────────────────────────────────────────────────────────────────
    # path('grade/<int:enrollment_id>/add/',  views.add_grade,    name='add_grade'),
    # path('grade/<int:grade_id>/edit/',      views.edit_grade,   name='edit_grade'),

    # # ── Assignment ────────────────────────────────────────────────────────────
    # path('assignment/<int:course_id>/create/',      views.create_assignment, name='create_assignment'),
    # path('assignment/<int:assignment_id>/',          views.assignment_detail, name='assignment_detail'),
    # path('assignment/<int:assignment_id>/edit/',     views.edit_assignment,   name='edit_assignment'),
    # path('assignment/<int:assignment_id>/delete/',   views.delete_assignment, name='delete_assignment'),
    # path('assignment/<int:assignment_id>/submit/',   views.submit_assignment, name='submit_assignment'),
    # path('assignment/<int:assignment_id>/submissions/', views.view_submissions, name='view_submissions'),

    # # ── Announcement ──────────────────────────────────────────────────────────
    # path('announcement/create/',                    views.make_announcement,   name='make_announcement'),
    # path('announcement/<int:announcement_id>/edit/', views.edit_announcement,  name='edit_announcement'),
    # path('announcement/<int:announcement_id>/delete/', views.delete_announcement, name='delete_announcement'),

    # # ── User management (staff only) ──────────────────────────────────────────
    # path('user/<int:user_id>/edit/',    views.edit_user,    name='edit_user'),