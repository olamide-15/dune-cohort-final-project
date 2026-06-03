from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from datetime import date


# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICE = [
        ('student', 'Student'),
        ('parent', 'Parent'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICE)
    date_of_birth = models.DateField(default='2000-01-01')
    phone = models.CharField(max_length=20, blank=True)
    GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    profile_picture = models.ImageField(
            upload_to='profile_pictures/',
            null=True,
            blank=True
        )
    class_name = models.CharField(max_length=20, blank=True)
    children = models.ManyToManyField('self', blank=True,)

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
    
    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_parent(self):
        return self.role == 'parent'

    @property
    def is_staff_member(self):       
        return self.role == 'staff'
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None


class Course(models.Model):
    title   = models.CharField(max_length=100)
    code    = models.CharField(max_length=20)
    files = models.FileField(upload_to='courses/', blank=True, null=True)    
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        limit_choices_to={'role': 'staff'},
        related_name='courses_taught'
    )

    def __str__(self):
        return f"{self.code} — {self.title} -{self.files}"


class Enrollment(models.Model):
    LEVEL_CHOICES = (
        {'1st', '100'},
        {'1st', '200'},
        {'1st', '300'},
        {'1st', '400'},
    )
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='enrollments'
    )
    course  = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    date    = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('student', 'course')  # a student can't enroll in the same course twice

    def __str__(self):
        return f"{self.student.get_full_name()} enrolled in {self.course.title}"
class Grade(models.Model):
    TERM_CHOICES = [
        ('1st', '1st Term'),
        ('2nd', '2nd Term'),
        ('3rd', '3rd Term'),
    ]
    enrollment  = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='grades'
    )
    score       = models.DecimalField(max_digits=5, decimal_places=2)
    term        = models.CharField(max_length=3, choices=TERM_CHOICES)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('enrollment', 'term')  # one grade per term per enrollment

    def __str__(self):
        return f"{self.enrollment.student.get_full_name()} — {self.term}: {self.score}%"


class Assignment(models.Model):
    course   = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    title    = models.CharField(max_length=200)
    due_date = models.DateField()
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.title} ({self.course.code})"
    
class AssignmentSubmission(models.Model):
    assignment   = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    student      = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='submissions'
    )
    submitted    = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(null=True, blank=True)
    file         = models.FileField(upload_to='submissions/', null=True, blank= True)

    class Meta:
        unique_together = ('assignment', 'student')  # one submission per student per assignment

    def __str__(self):
        status = "submitted" if self.submitted else "pending"
        return f"{self.student.get_full_name()} — {self.assignment.title} ({status})"
    
class Announcement(models.Model):
    AUDIENCE_CHOICES = [
        ('all',     'Everyone'),
        ('student', 'Students only'),
        ('parent',  'Parents only'),
        ('staff',   'Staff only'),
    ]
    title      = models.CharField(max_length=200)
    body       = models.TextField()
    audience   = models.CharField(max_length=10, choices=AUDIENCE_CHOICES, default='all')
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='announcements'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} → {self.audience}"
    
# class studentprofil
