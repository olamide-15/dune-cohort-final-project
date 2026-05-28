from django.urls import path
from . import views
from .views import StudentDetailAPIView, StudentListAPIView

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.course_list, name= 'course_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_details'),
    
    # path('assignment/<int:course_id>/create/',      views.create_assignment, name='create_assignment'),

    path('assignment/<int:course_pk>/create/',      views.assignment_create, name='assignment_create'),
    path('assignment/<int:assignment_pk>/',          views.assignment_detail, name='assignment_detail'),
    path('assignment/<int:assignment_pk>/edit/',     views.assignment_update,   name='edit_assignment'),
    path('assignment/<int:assignment_pk>/delete/',   views.delete_assignment, name='delete_assignment'),

    path('api/students/', StudentListAPIView.as_view(), name='api-student-list'),
    path('api/students/<int:pk>/', StudentDetailAPIView.as_view(), name='api-student-details')

    # path('assignment/<int:assignment_id>/submit/',   views.submit_assignment, name='submit_assignment'),
    # path('assignment/<int:assignment_id>/submissions/', views.view_submissions, name='view_submissions'),



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

]
