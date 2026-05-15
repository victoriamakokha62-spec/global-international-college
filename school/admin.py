from django.contrib import admin
from .models import StudentProfile, News, ContactMessage, AdmissionApplication, Event, Payment

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'enrollment_number', 'grade', 'enrolled_date')
    search_fields = ('user__first_name', 'user__last_name', 'enrollment_number')
    list_filter = ('grade', 'enrolled_date')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date', 'is_published')
    search_fields = ('title', 'content')
    list_filter = ('created_date', 'is_published')
    readonly_fields = ('created_date', 'updated_date')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_date', 'is_read')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_date', 'is_read')
    readonly_fields = ('created_date',)


@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'desired_grade', 'status', 'submitted_date')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('status', 'desired_grade', 'submitted_date')
    readonly_fields = ('submitted_date',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')
    search_fields = ('title', 'location')
    list_filter = ('date',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('phone', 'amount', 'status', 'created_at')
    search_fields = ('phone', 'merchant_request_id', 'checkout_request_id', 'mpesa_receipt_number')
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at', 'callback_raw')
