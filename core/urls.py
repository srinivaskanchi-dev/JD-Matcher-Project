from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.upload_resume, name='upload_resume'),
    path('download/<int:user_input_id>/', views.download_ats_resume, name='download_ats_resume'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),

] 