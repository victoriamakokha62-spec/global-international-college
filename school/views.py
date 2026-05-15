from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import StudentProfile, News, ContactMessage, AdmissionApplication, Event
from .forms import ContactForm, AdmissionApplicationForm, StudentRegistrationForm, StudentProfileForm


def index(request):
    news = News.objects.filter(is_published=True)[:3]
    events = Event.objects.all()[:3]
    context = {'news': news, 'events': events}
    return render(request, 'school/index.html', context)


def about(request):
    return render(request, 'school/about.html')


def academics(request):
    return render(request, 'school/academics.html')


def admissions(request):
    if request.method == 'POST':
        form = AdmissionApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('admissions')
    else:
        form = AdmissionApplicationForm()
    return render(request, 'school/admissions.html', {'form': form})


def news(request):
    news_list = News.objects.filter(is_published=True)
    context = {'news_list': news_list}
    return render(request, 'school/news.html', context)


def news_detail(request, id):
    article = get_object_or_404(News, id=id, is_published=True)
    return render(request, 'school/news_detail.html', {'article': article})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'school/contact.html', {'form': form})


@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect('portal')
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('portal')
    else:
        form = StudentRegistrationForm()
    return render(request, 'school/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('portal')
    
    if request.method == 'POST':
        email_or_username = request.POST.get('email_or_username')
        password = request.POST.get('password')
        
        user = None
        try:
            user = User.objects.get(email=email_or_username)
        except:
            user = authenticate(request, username=email_or_username, password=password)
        
        if user and user.check_password(password):
            user = authenticate(request, username=user.username, password=password)
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('portal')
        else:
            messages.error(request, 'Invalid credentials!')
    
    return render(request, 'school/login.html')


@login_required(login_url='login')
def portal(request):
    try:
        student = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        # Redirect to complete profile
        messages.info(request, 'Please complete your profile first.')
        return redirect('edit_profile')
    
    context = {'student': student}
    return render(request, 'school/portal.html', context)


@login_required(login_url='login')
def edit_profile(request):
    try:
        student = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        student = None
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('portal')
    else:
        form = StudentProfileForm(instance=student)
    
    return render(request, 'school/edit_profile.html', {'form': form})


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')


from django.contrib.auth.models import User
