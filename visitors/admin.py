from django.contrib import admin
from .models import Visitor

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'mobile',
        'gender',
        'purpose',
        'visit_to',
        'hostel_or_office',
        'entry_time',
        'exit_time',
        'status',
    )
