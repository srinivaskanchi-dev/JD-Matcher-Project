from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import download_ats_resume, chat_api
from django.contrib.auth.views import LoginView
from core.forms import StyledLoginForm
from core.views import custom_logout_view


urlpatterns = [
    path('', views.home_view, name='home'),
    path('upload/', views.upload_resume, name='upload_resume'),
    path('download/<int:user_input_id>/', views.download_ats_resume, name='download_ats_resume'),
    path('logout/', custom_logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
    path('download-ats-resume/<int:user_input_id>/', download_ats_resume, name='download_ats_resume'),
    path(
    'login/',
    LoginView.as_view(
        template_name='core/login.html',
        authentication_form=StyledLoginForm,
        redirect_authenticated_user=True,
        next_page='upload_resume'
    ),
    name='login'
    ),
    path('chat-api/', views.chat_api, name='chat_api'),
    path('about/', views.about_view, name='about'),
    path('faq/', views.faq_view, name='faq'),
    path('privacy/', views.privacy_view, name='privacy'),
] 