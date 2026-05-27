from django import forms
from django.utils import timezone
from .models import CustomUser, Course,Grade, Announcement,Assignment, Enrollment


class EditUserForm(forms.ModelForm):
    class meta:
        model = CustomUser
        fields = '__all__'


class GradeForm(forms.ModelForm):
    class Meta:
        model= Grade
        fields = ['term', 'score']

    def clean_score(self):
        score = self.cleaned_data.get('score')
        if score < 0 or score > 100:
            raise forms.ValidationError('score must be between 0 and 100')
        return score

class AssignmentForm(forms.ModelForm):
    class meta:
        model = Assignment
        fields = ['title', 'due_date']

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_data')
        if due_date < timezone.now().date():
            raise forms.ValidationError('Due date cannot be in the past')
        
class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['date']
        
        