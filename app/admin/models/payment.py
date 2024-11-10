# admin.py
from django.contrib import admin

from app.models.payment import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'course', 'phone_number', 'payment_date')
    search_fields = ('full_name', 'phone_number')
    list_filter = ('gender', 'payment_date')
    readonly_fields = ('payment_date',)  # Ngăn sửa trường này trong admin

