# Generated by Django 5.1.6 on 2025-05-26 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pageindex', '0005_job_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('job_title', models.CharField(max_length=100)),
                ('company', models.CharField(blank=True, max_length=100, null=True)),
                ('message', models.TextField()),
                ('photo', models.ImageField(default='testimonials/default.jpg', upload_to='testimonials/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
