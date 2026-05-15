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
            user = form.save(commit=False)
            # Deactivate account until it is confirmed via email
            user.is_active = False
            # If username is required, create one from email
            if not user.username:
                user.username = user.email.split('@')[0]
            user.save()

            # send verification email
            current_site = get_current_site(request)
            subject = 'Activate Your Global International College Account'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = request.build_absolute_uri(f"/register/activate/{uid}/{token}/")
            message = render_to_string('school/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'activation_link': activation_link,
            })
            send_mail(subject, message, None, [user.email])

            messages.success(request, 'Registration successful! Check your email to activate your account.')
            return redirect('login')
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
            if not user.is_active:
                messages.error(request, 'Account not activated. Check your email for the activation link.')
                return render(request, 'school/login.html')
            user = authenticate(request, username=user.username, password=password)
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('portal')
        else:
            messages.error(request, 'Invalid credentials!')
    
    return render(request, 'school/login.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated. You can now log in.')
        return redirect('login')
    else:
        return render(request, 'school/activation_invalid.html')


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
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import requests
import base64
import datetime
from decouple import config
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum
from django.utils import timezone
import csv
from django.http import HttpResponse
from django.shortcuts import Http404
from .models import Course, Lesson, Quiz, Question, QuizSubmission, AssignmentSubmission
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


def payment_page(request):
    return render(request, 'school/payment.html')


def _get_mpesa_token():
    """Obtain an OAuth token from Safaricom (sandbox or live depending on keys)."""
    consumer_key = config('MPESA_CONSUMER_KEY', default='')
    consumer_secret = config('MPESA_CONSUMER_SECRET', default='')
    oauth_url = config('MPESA_OAUTH_URL', default='https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials')

    auth = requests.auth.HTTPBasicAuth(consumer_key, consumer_secret)
    resp = requests.get(oauth_url, auth=auth)
    resp.raise_for_status()
    return resp.json().get('access_token')


@require_POST
@csrf_exempt
def mpesa_stk_push(request):
    """Initiate an M-Pesa STK Push (sandbox-ready).

    Expects POST with `phone` and `amount`.
    """
    try:
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        if not phone or not amount:
            return JsonResponse({'success': False, 'error': 'Missing phone or amount'}, status=400)

        # Config from environment
        shortcode = config('MPESA_SHORTCODE', default='174379')
        passkey = config('MPESA_PASSKEY', default='bfb279f9aa9bdbcf1...')
        callback_url = config('MPESA_CALLBACK_URL', default=request.build_absolute_uri('/mpesa/callback/'))

        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        password_bytes = f"{shortcode}{passkey}{timestamp}".encode('utf-8')
        password = base64.b64encode(password_bytes).decode('utf-8')

        token = _get_mpesa_token()
        headers = {'Authorization': f'Bearer {token}'}

        payload = {
            "BusinessShortCode": shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone,
            "PartyB": shortcode,
            "PhoneNumber": phone,
            "CallBackURL": callback_url,
            "AccountReference": "GICPayment",
            "TransactionDesc": "Payment to Global International College"
        }

        stk_url = config('MPESA_STK_URL', default='https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest')
        r = requests.post(stk_url, json=payload, headers=headers, timeout=15)
        r.raise_for_status()
        return JsonResponse({'success': True, 'response': r.json()})

    except requests.HTTPError as e:
        return JsonResponse({'success': False, 'error': str(e), 'response': getattr(e, 'response', {}).text}, status=500)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
def mpesa_callback(request):
    """Receive M-Pesa callback notifications (STK Push result)."""
    try:
        data = request.body.decode('utf-8')
        # In production parse JSON, validate signature, and update order status
        # For now just log and acknowledge
        print('MPESA CALLBACK RECEIVED:', data)
        return HttpResponse(status=200)
    except Exception as e:
        print('MPESA CALLBACK ERROR:', e)
        return HttpResponse(status=500)


@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    """Staff-only admin dashboard with basic analytics and links."""
    total_users = User.objects.count()
    total_students = StudentProfile.objects.count()
    total_payments = Payment.objects.count()
    successful_payments = Payment.objects.filter(status='success').aggregate(total=Sum('amount'))['total'] or 0
    failed_payments = Payment.objects.filter(status='failed').count()

    # payments per day for last 7 days
    today = timezone.now().date()
    labels = []
    data = []
    for i in range(6, -1, -1):
        day = today - timezone.timedelta(days=i)
        labels.append(day.strftime('%b %d'))
        day_sum = Payment.objects.filter(created_at__date=day, status='success').aggregate(total=Sum('amount'))['total'] or 0
        data.append(float(day_sum))

    recent_payments = Payment.objects.order_by('-created_at')[:10]

    context = {
        'total_users': total_users,
        'total_students': total_students,
        'total_payments': total_payments,
        'successful_payments_amount': successful_payments,
        'failed_payments_count': failed_payments,
        'chart_labels': labels,
        'chart_data': data,
        'recent_payments': recent_payments,
    }
    return render(request, 'school/admin_dashboard.html', context)


@user_passes_test(lambda u: u.is_staff)
def export_payments_csv(request):
    """Export payments as CSV (staff only)."""
    payments = Payment.objects.order_by('-created_at')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="payments.csv"'

    writer = csv.writer(response)
    writer.writerow(['id', 'phone', 'amount', 'status', 'merchant_request_id', 'checkout_request_id', 'mpesa_receipt_number', 'result_code', 'result_desc', 'created_at'])
    for p in payments:
        writer.writerow([p.id, p.phone, p.amount, p.status, p.merchant_request_id or '', p.checkout_request_id or '', p.mpesa_receipt_number or '', p.result_code or '', p.result_desc or '', p.created_at])

    return response


@user_passes_test(lambda u: u.is_staff)
def teacher_dashboard(request):
    courses = Course.objects.filter(created_by=request.user)
    my_lessons = Lesson.objects.filter(created_by=request.user)[:10]
    my_quizzes = Quiz.objects.filter(created_by=request.user)[:10]
    context = {'courses': courses, 'my_lessons': my_lessons, 'my_quizzes': my_quizzes}
    return render(request, 'school/teacher_dashboard.html', context)


@user_passes_test(lambda u: u.is_staff)
@require_http_methods(['GET', 'POST'])
def manage_courses(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title:
            Course.objects.create(title=title, description=description, created_by=request.user)
            return redirect('manage_courses')

    courses = Course.objects.filter(created_by=request.user)
    return render(request, 'school/manage_courses.html', {'courses': courses})


@user_passes_test(lambda u: u.is_staff)
@require_http_methods(['GET', 'POST'])
def upload_lesson(request, course_id):
    try:
        course = Course.objects.get(id=course_id, created_by=request.user)
    except Course.DoesNotExist:
        raise Http404()

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        file = request.FILES.get('file')
        Lesson.objects.create(course=course, title=title, content=content, file=file, created_by=request.user)
        return redirect('manage_courses')

    return render(request, 'school/upload_lesson.html', {'course': course})


@user_passes_test(lambda u: u.is_staff)
@require_http_methods(['GET', 'POST'])
def create_quiz(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        title = request.POST.get('title')
        # For simplicity, accept one question in the form
        q_text = request.POST.get('question')
        q_answer = request.POST.get('answer')
        course = Course.objects.get(id=course_id, created_by=request.user)
        quiz = Quiz.objects.create(course=course, title=title, created_by=request.user)
        if q_text:
            Question.objects.create(quiz=quiz, text=q_text, correct_answer=q_answer)
        return redirect('teacher_dashboard')

    courses = Course.objects.filter(created_by=request.user)
    return render(request, 'school/create_quiz.html', {'courses': courses})


@user_passes_test(lambda u: u.is_staff)
def grade_assignments(request):
    submissions = AssignmentSubmission.objects.filter(lesson__course__created_by=request.user).order_by('-submitted_at')
    if request.method == 'POST':
        sub_id = request.POST.get('submission_id')
        grade = request.POST.get('grade')
        submission = AssignmentSubmission.objects.get(id=sub_id, lesson__course__created_by=request.user)
        submission.grade = grade
        submission.graded_by = request.user
        submission.save()
        return redirect('grade_assignments')

    return render(request, 'school/grade_assignments.html', {'submissions': submissions})
