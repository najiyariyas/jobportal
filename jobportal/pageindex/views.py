from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CombinedRegistrationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import EmployerProfile, JobSeekerProfile

# Create your views here.

def index(request):
    return render(request,'pageindex/index.html')  # appname/filename

def about(request):
    return render(request,'pageindex/about.html')

def job_list(request):
    return render(request,'pageindex/job_list.html')

def job_category(request):
    return render(request,'pageindex/job_category.html')

def testimonial(request):
    return render(request,'pageindex/testimonial.html')

def contact(request):
    return render(request,'pageindex/contact.html')

def register_user(request):
    if request.method == 'POST':
        form = CombinedRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # Save and get the user instance
            login(request, user)  # Auto-login the user
            messages.success(request, "Account created successfully.")

            # Redirect to the dashboard based on user role
            if hasattr(user, 'page_employerprofile'):
                return redirect('employer_dashboard')
            elif hasattr(user, 'page_jobseekerprofile'):
                return redirect('jobseeker_dashboard')
            else:
                return redirect('default_dashboard') 
        else:
            # Optional: show errors in console for debugging
            print(form.errors)
    else:
        form = CombinedRegistrationForm()

    return render(request, 'pageindex/register.html', {'form': form})




@login_required
def employer_dashboard(request):
    try:
        employer_profile = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        employer_profile = None
    return render(request, 'dashboard/employer_dashboard.html', {'employer_profile': employer_profile})

@login_required
def jobseeker_dashboard(request):
    try:
        jobseeker_profile = JobSeekerProfile.objects.get(user=request.user)
    except JobSeekerProfile.DoesNotExist:
        jobseeker_profile = None
    return render(request, 'dashboard/jobseeker_dashboard.html', {'jobseeker_profile': jobseeker_profile})
