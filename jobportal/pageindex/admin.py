from django.contrib import admin
from .models import User, EmployerProfile, JobSeekerProfile, Job, Application, Skill, JobCategory

admin.site.register(User)
admin.site.register(EmployerProfile)
admin.site.register(JobSeekerProfile)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Skill)
admin.site.register(JobCategory)
