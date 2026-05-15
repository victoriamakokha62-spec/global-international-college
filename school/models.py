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


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    merchant_request_id = models.CharField(max_length=100, null=True, blank=True)
    checkout_request_id = models.CharField(max_length=100, null=True, blank=True)
    mpesa_receipt_number = models.CharField(max_length=100, null=True, blank=True)
    result_code = models.IntegerField(null=True, blank=True)
    result_desc = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    callback_raw = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.phone} - {self.amount} ({self.status})"


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='lessons/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    correct_answer = models.TextField()

    def __str__(self):
        return self.text[:50]


class QuizSubmission(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    answers = models.TextField()  # JSON or simple text map
    score = models.FloatField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.quiz.title}"


class AssignmentSubmission(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='assignments/', null=True, blank=True)
    comment = models.TextField(blank=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.lesson.title}"


class Subject(models.Model):
    SUBJECT_CHOICES = [
        ('english', 'English'),
        ('arabic', 'Arabic'),
        ('kiswahili', 'Kiswahili'),
        ('af_somali', 'Af-Soomaali'),
        ('mathematics', 'Mathematics'),
    ]
    key = models.CharField(max_length=50, choices=SUBJECT_CHOICES, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class LearningResource(models.Model):
    RESOURCE_TYPES = [
        ('writing', 'Writing Lesson'),
        ('video', 'Video Lesson'),
        ('pdf', 'PDF / Document'),
        ('audio', 'Audio Lesson'),
        ('download', 'Downloadable File'),
    ]
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    content_text = models.TextField(blank=True)
    file = models.FileField(upload_to='learning_resources/', null=True, blank=True)
    video_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject.title} - {self.title}"
