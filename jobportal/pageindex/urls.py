from django.urls import path
from pageindex import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),  
    path('job_list/',views.job_list,name='joblist'),
    path('job_category/',views.job_category,name='category'),
    path('testimonial/',views.testimonial,name='testimonial'),
    path('contact/',views.contact,name='contact'),
    path('login/', auth_views.LoginView.as_view(template_name='pageindex/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='pageindex/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='pageindex/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='pageindex/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='pageindex/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='pageindex/password_reset_complete.html'), name='password_reset_complete'),
  
    path('register/', views.register_user, name='register_user'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('jobseeker/dashboard/', views.jobseeker_dashboard, name='jobseeker_dashboard'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)