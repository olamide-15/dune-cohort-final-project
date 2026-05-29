"""
URL configuration for smartstudy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include 
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair' ),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('portal.urls')),
    path('', include('account.urls')),
    path('api-auth/token/', obtain_auth_token, name='api-token'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



#     {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDA5NTc2OCwiaWF0IjoxNzgwMDA5MzY4LCJqdGkiOiJjNDhkM2ExZmQxZTY0MmQwOGQxMmJiMGY3MzBmYzc2NyIsInVzZXJfaWQiOiIxIn0.5m1kCg2ixmJxvS33BkflpD8SCY-MeHt5eaBSwvM5ico",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgwMDEwMjY4LCJpYXQiOjE3ODAwMDkzNjgsImp0aSI6IjcyYzFjZjM5YTg5NDRhNGU5MTY2Mjk2ZjVkNDNjZmYwIiwidXNlcl9pZCI6IjEifQ.K42IKuY30P7eAGcxmy9alR9b-hy4F29Ub_Mjde09bIY"
# }

#      "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDEzOTY0MCwiaWF0IjoxNzgwMDUzMjQwLCJqdGkiOiJlOGI3YzNhMmI0Yzc0MzBiOTIzNjE4NjgwZTQwOTg2OSIsInVzZXJfaWQiOiIxIn0.Amxy-w9XrFbhTzdhfLJYzVNs53wes6zLegs_GA1Kdww",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgwMDU0MTQwLCJpYXQiOjE3ODAwNTMyNDAsImp0aSI6IjI2MThkNzZhYTFjNjRmY2FiYzQ1N2E3M2YzOGNlOGNhIiwidXNlcl9pZCI6IjEifQ.uBrmL5F52WQMaMC5bQ4dOAVdemlAWziC7yvsznnpPtQ"