from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from functools import wraps
from .forms import AssignmentForm, GradeForm, EnrollmentForm
from .models import AssignmentSubmission,Assignment, Course, Enrollment, Grade
import json
from django.http import JsonResponse
from .models import CustomUser

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, CourseSerializer
from rest_framework import status
from rest_framework.decorators import api_view



# Create your views here.


def home(request):
    return render(request, 'portal/home.html')

def course_list(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'portal/course_list.html', context)

def course_list_json(request):
    courses = Course.objects.all()
    data =[{'id': c.id, 'title': c.title, 'code': c.code, 'teacher': c.teacher.get_full_name()if c.teacher else None} for c in courses]

    return JsonResponse(data, safe=False)

def course_details(request, pk):
    course = get_object_or_404(Course, pk= pk)
    context = {'course': course} 
    return render(request, 'portal/course_detail.html', context)

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


#  API VIEWS

# @api_view(['GET'])
# def student_list(request):
#     students = CustomUser.objects.filter(role='is_student')
#     serializer = UserSerializer(students, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def staff_list(request):
#     staffs = CustomUser.objects.filter(role='is_staff_member')
#     serializer = UserSerializer(staffs, many=True)
#     return Response(serializer.data) 


class StudentListAPIView(APIView):
    def get(self, request):        
        students = CustomUser.objects.filter(role='student')
        serializer =UserSerializer(students, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StudentDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk,role='student')
        except CustomUser.DoesNotExist:
            return None
        
    def get(self, request, pk):
        student = self.get_object(pk)
        if student is None:
            return Response({'error':'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(student)
        return Response(serializer.data)
    
    def put(self, request, pk):
            student = self.get_object(pk)
            if student is None:
                return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = UserSerializer(student, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        student = self.get_object(pk)
        if student is None:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        student.delete()
        # 204 No Content — success but no data to return
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# class StudentListAPIView(APIView):
#     def get(self, request):
#         # Step 1 - check if ANY users exist
#         all_users = CustomUser.objects.all()
#         print("Total users:", all_users.count())

#         # Step 2 - check what roles are stored
#         roles = CustomUser.objects.values_list('role', flat=True).distinct()
#         print("Roles in DB:", list(roles))

#         # Step 3 - filter based on actual role value
#         students = CustomUser.objects.filter(role='is_student')
#         print("Students found:", students.count())

#         serializer = UserSerializer(students, many=True)
#         return Response(serializer.data)
