from rest_framework import serializers
from .models import CustomUser, Course, Enrollment, Grade, Assignment, AssignmentSubmission, Announcement


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'phone', 'class_name']


class CourseSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'code', 'teacher']

    def get_teacher(self, obj):
        return obj.teacher.get_full_name() if obj.teacher else None


class EnrollmentSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    course  = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'date']


class GradeSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = Grade
        fields = ['id', 'course', 'term', 'score', 'recorded_at']

    def get_course(self, obj):
        return obj.enrollment.course.title


class AssignmentSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'due_date', 'course']

    def get_course(self, obj):
        return obj.course.title


class SubmissionSerializer(serializers.ModelSerializer):
    student    = serializers.SerializerMethodField()
    assignment = serializers.SerializerMethodField()
    course     = serializers.SerializerMethodField()

    class Meta:
        model = AssignmentSubmission
        fields = ['id', 'student', 'assignment', 'course', 'submitted', 'submitted_at', 'file']

    def get_student(self, obj):
        return obj.student.get_full_name()

    def get_assignment(self, obj):
        return obj.assignment.title

    def get_course(self, obj):
        return obj.assignment.course.code