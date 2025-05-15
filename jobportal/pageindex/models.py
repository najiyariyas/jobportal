from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class User(AbstractUser):
    is_employer = models.BooleanField(default=False)
    is_job_seeker = models.BooleanField(default=False)

    def __str__(self):
        return self.username

# EmployerProfile Model
class EmployerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='page_employerprofile')
    company_name = models.CharField(max_length=255, blank=True)
    company_website = models.URLField(blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)

    def __str__(self):
        return self.company_name

# JobSeekerProfile Model
class JobSeekerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='page_jobseekerprofile')
    resume = models.FileField(upload_to='resumes/')
    skills = models.ManyToManyField('Skill', blank=True)
    experience_years = models.PositiveIntegerField()
    education = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.user.username

# Job Model
class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    company = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name='jobs')
    location = models.CharField(max_length=100)
    skills = models.ManyToManyField('Skill', blank=True) 
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    job_type = models.CharField(
        max_length=50,
        choices=[
            ('Full-time', 'Full-time'),
            ('Part-time', 'Part-time'),
            ('Internship', 'Internship'),
            ('Contract', 'Contract')
        ]
    )
    posted_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} at {self.company.company_name}"

# Application Model
class Application(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Reviewed', 'Reviewed'),
        ('Interview', 'Interview Scheduled'),
        ('Rejected', 'Rejected'),
        ('Accepted', 'Accepted'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True, null=True)
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f'{self.applicant.username} - {self.job.title}'

# Skill Model
class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# JobCategory Model
class JobCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

