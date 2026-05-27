from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='account/login.html', next_page='dashboard'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/register/', views.register, name='register'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/parent/', views.parent_dashboard, name='parent_dashboard'),
    path('dashboard/staff/', views.staff_dashboard,name='staff_dashboard'),    
]
