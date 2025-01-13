from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('lmsapp.urls')),  # This will include Users, Books & Transaction API
    path('api/login/', auth_views.LoginView.as_view(), name='login'),  # Login view
    path('api/logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout view
]