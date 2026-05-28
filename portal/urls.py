from django.urls import path
from . import views
from .views import StudentDetailAPIView, StudentListAPIView, StudentCreateAPIView

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
    path('api/students/<int:pk>/', StudentDetailAPIView.as_view(), name='api-student-details'),
    path('students/create/', StudentCreateAPIView.as_view(), name='student-create')
]
