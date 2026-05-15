from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class StudentProfile(models.Model):
    GRADE_CHOICES = [
        ('1-3', 'Primary (1-3)'),
        ('4-5', 'Primary (4-5)'),
        ('6-8', 'Middle School'),
        ('9-10', 'High School (9-10)'),
        ('11-12', 'High School (11-12)'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    enrollment_number = models.CharField(max_length=20, unique=True)
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES)
    date_of_birth = models.DateField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    parent_name = models.CharField(max_length=100)
    parent_email = models.EmailField()
    parent_phone = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='student_profiles/', null=True, blank=True)
    enrolled_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.enrollment_number}"


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_date']
    
    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_date']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


class AdmissionApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    desired_grade = models.CharField(max_length=10, choices=StudentProfile.GRADE_CHOICES)
    current_school = models.CharField(max_length=100)
    parent_name = models.CharField(max_length=100)
    parent_email = models.EmailField()
    parent_phone = models.CharField(max_length=20)
    message = models.TextField()
    submitted_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    documents = models.FileField(upload_to='admissions/', null=True, blank=True, 
                                validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])])
    
    class Meta:
        ordering = ['-submitted_date']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.status}"


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    
    class Meta:
        ordering = ['date']
    
    def __str__(self):
        return self.title