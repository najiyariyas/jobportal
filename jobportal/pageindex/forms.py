from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, JobSeekerProfile, EmployerProfile

class CombinedRegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('employer', 'Employer'),
        ('job_seeker', 'Job Seeker'),
    )

    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.Select,
        label="Register As"
    )

    # Common fields
    email = forms.EmailField(required=True)

    # Job seeker fields
    resume = forms.FileField(required=False)
    experience_years = forms.IntegerField(required=False, min_value=0)
    education = forms.CharField(required=False, max_length=255)
    seeker_location = forms.CharField(required=False, max_length=100)

    # Employer fields
    company_name = forms.CharField(required=False, max_length=255)
    company_website = forms.URLField(required=False)
    company_description = forms.CharField(required=False, widget=forms.Textarea)
    employer_location = forms.CharField(required=False, max_length=255)
    contact_number = forms.CharField(required=False, max_length=20)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Hide employer/job seeker fields initially; show based on POST data
        user_type = self.data.get('user_type') or self.initial.get('user_type')
        
        if user_type == 'job_seeker':
            # Hide employer fields
            for field in ['company_name', 'company_website', 'company_description', 'employer_location', 'contact_number']:
                self.fields.pop(field)
        elif user_type == 'employer':
            # Hide job seeker fields
            for field in ['resume', 'experience_years', 'education', 'seeker_location']:
                self.fields.pop(field)

    def save(self, commit=True):
      user = super().save(commit=False)
      user.email = self.cleaned_data['email']

      if commit:
        user.save()

        user_type = self.cleaned_data['user_type']

        if user_type == 'job_seeker':
            user.is_job_seeker = True
            user.save()
            JobSeekerProfile.objects.create(
                user=user,
                resume=self.files.get('resume'),
                experience_years=self.cleaned_data.get('experience_years') or 0,
                education=self.cleaned_data.get('education', ''),
                location=self.cleaned_data.get('seeker_location', '')
            )
        elif user_type == 'employer':
            user.is_employer = True
            user.save()
            EmployerProfile.objects.create(
                user=user,
                company_name=self.cleaned_data.get('company_name', ''),
                company_website=self.cleaned_data.get('company_website', ''),
                company_description=self.cleaned_data.get('company_description', ''),
                location=self.cleaned_data.get('employer_location', ''),
                contact_number=self.cleaned_data.get('contact_number', '')
            )

      return user
