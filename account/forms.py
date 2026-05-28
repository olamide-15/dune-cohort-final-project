from django import forms
from django.contrib.auth.forms import UserCreationForm
from portal.models import CustomUser

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class':'form-input'}))
    widget = {
        username : forms.TextInput(attrs={'placeholder':'Username', }),
        password : forms.TextInput(attrs={'placeholder':'password'})
    }
class RegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=[
         ('student', 'Student'),
         ('parent', 'Parent'),
    ])
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'phone', 'class_name', 'password1','password2']

    def clean_email(self):
            email = self.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email).exists():
                raise forms.ValidationError('This email is already registered.')
            return email

    def clean_class_name(self):
            role       = self.cleaned_data.get('role')
            class_name = self.cleaned_data.get('class_name')
            if role != 'student' and class_name:
                raise forms.ValidationError('Only students should have a class name.')
            return class_name