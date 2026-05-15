from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('academics/', views.academics, name='academics'),
    path('admissions/', views.admissions, name='admissions'),
    path('news/', views.news, name='news'),
    path('news/<int:id>/', views.news_detail, name='news_detail'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('register/activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('portal/', views.portal, name='portal'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('payment/', views.payment_page, name='payment'),
    path('mpesa/stk_push/', views.mpesa_stk_push, name='mpesa_stk_push'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/payments/export_csv/', views.export_payments_csv, name='export_payments_csv'),
    # Teacher system
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/courses/', views.manage_courses, name='manage_courses'),
    path('teacher/courses/<int:course_id>/lessons/upload/', views.upload_lesson, name='upload_lesson'),
    path('teacher/quizzes/create/', views.create_quiz, name='create_quiz'),
    path('teacher/assignments/grade/', views.grade_assignments, name='grade_assignments'),
    path('learning/', views.learning_content, name='learning_content'),
    path('learning/subject/<slug:key>/', views.subject_resources, name='subject_resources'),
]
