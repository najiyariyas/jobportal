from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import CombinedRegistrationForm,EmployerProfileForm,JobSeekerProfileForm
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import EmployerProfile, JobSeekerProfile,Job
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail






# Create your views here.


def index(request):
    featured_jobs = Job.objects.filter(is_active=True).order_by('-posted_at')[:5]
    full_time_jobs = Job.objects.filter(is_active=True, job_type='Full-time')[:5]
    part_time_jobs = Job.objects.filter(is_active=True, job_type='Part-time')[:5]

    context = {
        'featured_jobs': featured_jobs,
        'full_time_jobs': full_time_jobs,
        'part_time_jobs': part_time_jobs,
    }
    return render(request, 'pageindex/index.html', context)


def about(request):
    return render(request, 'pageindex/about.html')

def job_list(request):
    jobs = Job.objects.filter(is_active=True).order_by('-posted_at')
    return render(request, 'pageindex/job_list.html', {'jobs': jobs})

@login_required(login_url='login')
def job_category(request):
    return render(request, 'pageindex/job_category.html')

@login_required(login_url='login')
def testimonial(request):
    return render(request, 'pageindex/testimonial.html')

@login_required(login_url='login')
def contact(request):
    return render(request, 'pageindex/contact.html')

def register_user(request):
    if request.method == 'POST':
        form = CombinedRegistrationForm(request.POST, request.FILES)
        
        # Debugging form validity and errors
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")

            
            if hasattr(user, 'page_employerprofile'):
                return redirect('employer_dashboard')
            elif hasattr(user, 'page_jobseekerprofile'):
                return redirect('jobseeker_dashboard')
            else:
                return redirect('default_dashboard')
        else:
            # Form errors printed for debugging
            print("Form Errors:", form.errors)  

            # Show errors to the user
            messages.error(request, "Please correct the errors below.")
            return render(request, 'pageindex/register.html', {'form': form})

    else:
        form = CombinedRegistrationForm()
    
    return render(request, 'pageindex/register.html', {'form': form})


def logout(request):
    auth_logout(request)  
    messages.success(request, "You have been logged out successfully.")
    return redirect('index')


# Employer and Job Seeker dashboard views

@login_required
def general_dashboard(request):
    # Check if the user has an employer profile
    if EmployerProfile.objects.filter(user=request.user).exists():
        return redirect('employer_dashboard')
    elif JobSeekerProfile.objects.filter(user=request.user).exists():
        return redirect('jobseeker_dashboard')
    else:
        
        return redirect('index')  
@login_required
def employer_dashboard(request):
    try:
        employer_profile = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        messages.error(request, "No employer profile found.")
        return redirect('index')

    context = {
        'employer_profile': employer_profile,
    }
    return render(request, 'dashboard/employer_dashboard.html', context)
@login_required
def jobseeker_dashboard(request):
    jobseeker_profile = request.user.page_jobseekerprofile 

    available_jobs = Job.objects.filter(is_active=True)

    context = {
        'jobseeker_profile': jobseeker_profile,
        'available_jobs': available_jobs,
    }
    return render(request, 'dashboard/jobseeker_dashboard.html', context)



def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'pageindex/job_details.html', {'job': job})


@login_required
def edit_employer_profile(request):
    print("DEBUG - Logged in user:", request.user.username)
    print("DEBUG - is_employer:", getattr(request.user, 'is_employer', None))
    print("DEBUG - has EmployerProfile:", hasattr(request.user, 'page_employerprofile'))
    if not request.user.is_employer:
        raise PermissionDenied("Only employers can edit profiles.")

    try:
        profile = request.user.page_employerprofile
    except EmployerProfile.DoesNotExist:
        return redirect('employer_profile_setup')

    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('employer_dashboard')
    else:
        form = EmployerProfileForm(instance=profile)

    return render(request, 'employer/edit_employer_profile.html', {'form': form})
from .forms import JobForm



@login_required
def post_job(request):
    print("=== POST JOB VIEW HIT ===")
    print("User:", request.user)
    print("is_employer:", request.user.is_employer)
    print("is_authenticated:", request.user.is_authenticated)
   

    if not getattr(request.user, 'is_employer', False):
        raise PermissionDenied("Only employers can post jobs.")

    if not hasattr(request.user, 'page_employerprofile'):
        return redirect('employer_profile_setup')

    employer_profile = request.user.page_employerprofile

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = employer_profile
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect('employer_dashboard')
    else:
        form = JobForm()

    return render(request, 'employer/post_job.html', {'form': form})

@login_required
def employer_profile_setup(request):
    if not request.user.is_employer:
        raise PermissionDenied("Only employers can set up a profile.")

    # Prevent duplicate profile creation
    if hasattr(request.user, 'page_employerprofile'):
        messages.info(request, "Profile already exists.")
        return redirect('employer_dashboard')

    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Employer profile created successfully.")
            return redirect('employer_dashboard')
    else:
        form = EmployerProfileForm()

    return render(request, 'employer/employer_profile_setup.html', {'form': form})





import logging

logger = logging.getLogger(__name__)
@login_required
def contact_view(request):
    print("🔔 contact_view is being called.")
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        print("📩 Form submitted successfully.")
        print(f"Name: {name}, Email: {email}, Subject: {subject}, Message: {message}")

        try:
            full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

            send_mail(
                subject,
                full_message,
                'najiya18@gmail.com',
                ['najiya18@gmail.com'],
                fail_silently=False,
            )
            print("✅ Email sent successfully!")
            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            messages.error(request, 'There was a problem sending your message.')

        return redirect('contact')

    return render(request, 'pageindex/contact.html')

@login_required
def my_profile(request):
    if EmployerProfile.objects.filter(user=request.user).exists():
        return redirect('employer_dashboard')
    elif JobSeekerProfile.objects.filter(user=request.user).exists():
        return redirect('jobseeker_dashboard')
    else:
        return redirect('index')
@login_required
def edit_jobseeker_profile(request):
    profile = request.user.page_jobseekerprofile  # updated related_name
    if request.method == 'POST':
        form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('jobseeker_dashboard')  # make sure this name matches your URL
    else:
        form = JobSeekerProfileForm(instance=profile)
    return render(request, 'jobseeker/edit_jobseeker_profile.html', {'form': form})


@login_required(login_url='login')
def job_by_skill(request):
    a = request.GET.get('skill')
    jobs = Job.objects.all()
    if a:
        jobs = jobs.filter(skills__name__icontains=a).distinct()
    return render(request, 'pageindex/job_by_skill.html', {'jobs': jobs, 'query': a})

# Search by Location
@login_required(login_url='login')
def job_by_location(request):
    a = request.GET.get('location')
    jobs = Job.objects.filter(location__icontains=a) if a else Job.objects.all()
    return render(request, 'pageindex/job_by_location.html', {'jobs': jobs, 'query': a})

# Search by Designation (title)
@login_required(login_url='login')
def job_by_designation(request):
    a = request.GET.get('designation')
    jobs = Job.objects.filter(title__icontains=a) if a else Job.objects.all()
    return render(request, 'pageindex/job_by_designation.html', {'jobs': jobs, 'query': a})

@login_required
def test_user_type(request):
    return HttpResponse(f"User: {request.user.username}, Is Employer: {getattr(request.user, 'is_employer', None)}")











