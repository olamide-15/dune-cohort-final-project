from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='account/login.html', next_page='dashboard'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/register/', views.register, name='register'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/student/courses/', views.student_courses, name='student_courses'),
    path('dashboard/student/assignments/', views.student_assignments, name='student_assignments'),
    path('dashboard/student/assignments/submit/<int:submission_id>/', views.student_submit_assignment, name='student_submit_assignment'),
    path('dashboard/student/profile/', views.student_profile, name='student_profile'),

    path('dashboard/parent/', views.parent_dashboard, name='parent_dashboard'),

    
    path('dashboard/staff/', views.staff_dashboard,name='staff_dashboard'),    
    path('dashboard/staff/students/', views.staff_student_profiles, name='staff_student_profiles'),
    path('dashboard/staff/courses/add/', views.staff_add_course, name='staff_add_course'),
    path('dashboard/staff/grades/add/', views.staff_add_grade, name='staff_add_grade'),
    path('dashboard/staff/submissions/', views.staff_view_submissions, name='staff_view_submissions'),
    path('dashboard/staff/announcements/add/', views.staff_add_announcement, name='staff_add_announcement'),
    path('dashboard/staff/assignment/add/', views.staff_add_assignment, name='staff_add_assignment'),

    path('dashboard/admin/', views.admin_dashboard,  name='admin_dashboard'),
    path('dashboard/admin/enrollments/', views.admin_enrollments,  name='admin_enrollments'),
    path('dashboard/admin/enrollments/add/',views.admin_enroll_student,name='admin_enroll_student'),
    path('dashboard/admin/enrollments/remove/<int:enrollment_id>/', views.admin_remove_enrollment, name='admin_remove_enrollment'),
    path('dashboard/admin/students/add/', views.admin_add_student, name='admin_add_student'),
]
