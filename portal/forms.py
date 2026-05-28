from django import forms
from django.utils import timezone
from .models import CustomUser, Course,Grade, Announcement,Assignment, Enrollment, AssignmentSubmission
from django.contrib.auth.hashers import make_password


class EditUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'code']

class GradeForm(forms.ModelForm):
    class Meta:
        model= Grade
        fields = ['term', 'score', 'enrollment']

    def clean_score(self):
        score = self.cleaned_data.get('score')
        if score < 0 or score > 100:
            raise forms.ValidationError('score must be between 0 and 100')
        return score

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'due_date']

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_data')
        if due_date < timezone.now().date():
            raise forms.ValidationError('Due date cannot be in the past')
        return due_date
        
class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['date']

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'body', 'audience']

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['file']


class AdminEnrollmentForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='student').order_by('last_name')
    )

    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'date']


class AdminAddStudentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'class_name', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'                              # always set to student
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user        