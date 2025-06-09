from django.urls import path
from pageindex import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),  
    path('jobs/', views.job_list, name='job_list'),
    path('job_category/',views.job_category,name='category'),
    path('testimonial/',views.testimonial,name='testimonial'),
    path('login/', auth_views.LoginView.as_view(template_name='pageindex/login.html'), name='login'),
    path('logout/', views.logout, name='logout'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
  
    path('register/', views.register_user, name='register_user'),
    path('dashboard/', views.general_dashboard, name='general_dashboard'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('jobseeker/dashboard/', views.jobseeker_dashboard, name='jobseeker_dashboard'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('employer/post-job/', views.post_job, name='post_job'),
    path('employer/profile/setup/', views.employer_profile_setup, name='employer_profile_setup'),
    path('employer/profile/edit/', views.edit_employer_profile, name='edit_employer_profile'),
    path('contact/', views.contact_view, name='contact'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('dashboard/edit_jobseeker_profile/', views.edit_jobseeker_profile, name='edit_jobseeker_profile'),
    path('dashboard/edit_employer_profile/', views.edit_employer_profile, name='edit_employer_profile'),
    path('jobs/skills/', views.job_by_skill, name='job_by_skill'),
    path('jobs/location/', views.job_by_location, name='job_by_location'),
    path('jobs/designation/', views.job_by_designation, name='job_by_designation'),  
    path('test-user/', views.test_user_type),




]
