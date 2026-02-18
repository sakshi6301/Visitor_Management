from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import timedelta
import base64

from .models import Visitor
from .models import Employee, EmployeeAttendance


# =====================
# HOME
# =====================
def home(request):
    return render(request, 'visitors/home.html')



# =====================
# REGISTER
# =====================
def register_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=email).exists():
            messages.error(request, "User with this email already exists.")
            return redirect('register')

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

    return render(request, 'visitors/registration.html')


# =====================
# LOGIN
# =====================



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "users/login.html")



# =====================
# LOGOUT
# =====================
def logout_view(request):
    name = request.user.first_name or request.user.username
    logout(request)
    messages.success(request, f"Logged out successfully, {name}")
    return redirect('login')


# =====================
# DASHBOARD (RECEPTIONIST VIEW - ALL VISITORS)
# =====================
@login_required
def dashboard(request):
    now = timezone.now()

    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = today_start - timedelta(days=1)
    last_7_days_start = today_start - timedelta(days=7)

    # Show ALL visitors (not filtered by user)
    visitors = Visitor.objects.all()

    # Alert: Visitors staying too long (more than 4 hours)
    long_staying_visitors = visitors.filter(
        status='IN',
        entry_time__lt=now - timedelta(hours=4)
    )

    # Recent visitors (last 5)
    recent_visitors = visitors.order_by('-entry_time')[:5]

    context = {
        'total_today': visitors.filter(entry_time__gte=today_start).count(),
        'total_yesterday': visitors.filter(
            entry_time__gte=yesterday_start,
            entry_time__lt=today_start
        ).count(),
        'total_last_7_days': visitors.filter(entry_time__gte=last_7_days_start).count(),
        'total_visitors': visitors.count(),
        'long_staying_visitors': long_staying_visitors,
        'recent_visitors': recent_visitors,
    }

    return render(request, 'visitors/dashboard.html', context)


# =====================
# ADD VISITOR (WITH NOTIFICATIONS)
# =====================
@login_required
def add_visitor(request):
    if request.method == "POST":

        signature_data = request.POST.get("signature_data")
        signature_file = None

        if signature_data:
            try:
                format, imgstr = signature_data.split(";base64,")
                ext = format.split("/")[-1]
                signature_file = ContentFile(
                    base64.b64decode(imgstr),
                    name=f"signature_{timezone.now().timestamp()}.{ext}"
                )
            except Exception:
                signature_file = None

        # Handle scheduled entry time
        scheduled_time = request.POST.get('scheduled_entry_time')
        if scheduled_time:
            from datetime import datetime
            entry_time = timezone.make_aware(datetime.fromisoformat(scheduled_time))
        else:
            entry_time = timezone.now()

        visitor = Visitor.objects.create(
            name=request.POST.get('name'),
            mobile=request.POST.get('mobile'),
            email=request.POST.get('email'),
            gender=request.POST.get('gender'),
            purpose=request.POST.get('purpose'),
            visit_to=request.POST.get('visit_to'),
            hostel_or_office=request.POST.get('hostel_or_office'),
            address=request.POST.get('address'),
            aadhaar=request.POST.get('aadhaar'),
            photo=request.FILES.get('photo'),
            signature=signature_file,
            created_by=request.user,
            entry_time=entry_time
        )

        # Send notifications
        from .notifications import (
            send_host_notification_email,
            send_visitor_confirmation_email,
            send_host_notification_sms,
            send_visitor_confirmation_sms
        )
        
        host_email = request.POST.get('host_email')
        host_mobile = request.POST.get('host_mobile')
        
        # Email notifications
        if host_email:
            send_host_notification_email(visitor, host_email)
        send_visitor_confirmation_email(visitor)
        
        # SMS notifications
        if host_mobile:
            send_host_notification_sms(visitor, host_mobile)
        send_visitor_confirmation_sms(visitor)

        messages.success(request, "Visitor added successfully. Notifications sent.")
        return redirect('visitor_list')

    return render(request, 'visitors/visitor_entry.html')


# =====================
# VISITOR LIST (ALL VISITORS + PAGINATION)
# =====================
@login_required
def visitor_list(request):
    # Show ALL visitors (not filtered by user)
    visitors = Visitor.objects.all().order_by('-entry_time')

    # Pagination
    paginator = Paginator(visitors, 10)  # 10 visitors per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'visitors': page_obj,
        'total': visitors.count(),
        'in_count': visitors.filter(status='IN').count(),
        'out_count': visitors.filter(status='OUT').count(),
    }

    return render(request, 'visitors/visitor_list.html', context)


# =====================
# CHECKOUT VISITOR (ANY RECEPTIONIST CAN CHECKOUT)
# =====================
@login_required
def checkout_visitor(request, visitor_id):
    # Any receptionist can checkout any visitor
    visitor = get_object_or_404(Visitor, id=visitor_id)

    if visitor.status == 'IN':
        visitor.status = 'OUT'
        visitor.exit_time = timezone.now()
        visitor.save()
        messages.success(request, "Visitor checked out successfully.")

    return redirect('visitor_list')


# =====================
# VISITOR REPORT (ALL VISITORS)
# =====================
@login_required
def visitor_report(request):
    # Show ALL visitors
    visitors = Visitor.objects.all().order_by('-entry_time')

    return render(request, 'visitors/visitor_report.html', {
        'visitors': visitors
    })


@login_required
def profile(request):
    user = request.user

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # 🔥 username duplicate check
        if User.objects.exclude(id=user.id).filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("profile")

        user.username = username

        if password:
            user.set_password(password)

        user.save()
        messages.success(request, "Profile updated. Please login again.")
        return redirect("login")

    return render(request, "visitors/profile.html")



# =========================
# Employee List (WITH PAGINATION)
# =========================

@login_required
def employee_list(request):
    employees = Employee.objects.all().order_by("-created_at")

    employee_data = []
    for emp in employees:
        attendance = EmployeeAttendance.objects.filter(
            employee=emp,
            date=timezone.localdate()
        ).first()

        employee_data.append({
            "emp": emp,
            "in_time": attendance.in_time if attendance else None,
            "out_time": attendance.out_time if attendance else None,
        })

    # Pagination
    paginator = Paginator(employee_data, 10)  # 10 employees per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "visitors/employee_list.html", {
        "employee_data": page_obj
    })

# =========================
# Add Employee
# =========================

import base64
from django.core.files.base import ContentFile
from django.utils import timezone

@login_required
def add_employee(request):
    if request.method == "POST":

        # ✅ Digital signature
        signature_file = None
        signature_data = request.POST.get("signature_data")

        if signature_data:
            format, imgstr = signature_data.split(";base64,")
            ext = format.split("/")[-1]
            signature_file = ContentFile(
                base64.b64decode(imgstr),
                name=f"emp_sign_{timezone.now().timestamp()}.{ext}"
            )

        Employee.objects.create(
            name=request.POST.get("name"),
            mobile=request.POST.get("mobile"),
            work_as=request.POST.get("work_as"),
            status=request.POST.get("status"),
            signature=signature_file
        )

        messages.success(request, "Employee added successfully")
        return redirect("employee_list")

    return render(request, "visitors/add_employee.html")





@login_required
def employee_checkin(request, emp_id):
    employee = get_object_or_404(Employee, id=emp_id)

    # today attendance already exists?
    attendance, created = EmployeeAttendance.objects.get_or_create(
        employee=employee,
        date=timezone.localdate()
    )

    if attendance.in_time:
        messages.warning(request, "Employee already checked IN")
    else:
        attendance.in_time = timezone.localtime().time()
        attendance.status = "IN"
        attendance.save()
        messages.success(request, "Employee checked IN successfully")

    return redirect("employee_list")


@login_required
def employee_checkout(request, emp_id):
    employee = get_object_or_404(Employee, id=emp_id)

    attendance = EmployeeAttendance.objects.filter(
        employee=employee,
        date=timezone.localdate()
    ).first()

    if not attendance or not attendance.in_time:
        messages.error(request, "Employee not checked IN yet")
    elif attendance.out_time:
        messages.warning(request, "Employee already checked OUT")
    else:
        attendance.out_time = timezone.localtime().time()
        attendance.status = "OUT"
        attendance.save()
        messages.success(request, "Employee checked OUT successfully")

    return redirect("employee_list")


# =========================
# Daily Summary Report (JSON API)
# =========================
@login_required
def daily_summary(request):
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    visitors = Visitor.objects.filter(
        created_by=request.user,
        entry_time__gte=today_start
    )
    
    summary = {
        'date': today_start.strftime('%Y-%m-%d'),
        'total_visitors': visitors.count(),
        'currently_in': visitors.filter(status='IN').count(),
        'checked_out': visitors.filter(status='OUT').count(),
        'long_staying': visitors.filter(
            status='IN',
            entry_time__lt=now - timedelta(hours=4)
        ).count(),
    }
    
    return JsonResponse(summary)


# =========================
# Dashboard Auto-Refresh API
# =========================
@login_required
def dashboard_stats(request):
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = today_start - timedelta(days=1)
    last_7_days_start = today_start - timedelta(days=7)
    
    visitors = Visitor.objects.filter(created_by=request.user)
    
    stats = {
        'total_today': visitors.filter(entry_time__gte=today_start).count(),
        'total_yesterday': visitors.filter(
            entry_time__gte=yesterday_start,
            entry_time__lt=today_start
        ).count(),
        'total_last_7_days': visitors.filter(entry_time__gte=last_7_days_start).count(),
        'total_visitors': visitors.count(),
        'long_staying_count': visitors.filter(
            status='IN',
            entry_time__lt=now - timedelta(hours=4)
        ).count(),
    }
    
    return JsonResponse(stats)


# =========================
# Analytics & Reports
# =========================
from django.db.models import Count, Q
from django.db.models.functions import TruncHour, TruncDate
import csv
from django.http import HttpResponse

@login_required
def analytics_dashboard(request):
    visitors = Visitor.objects.filter(created_by=request.user)
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=7)
    month_start = today_start - timedelta(days=30)
    
    # Department-wise analysis
    dept_stats = visitors.values('hostel_or_office').annotate(
        total=Count('id'),
        in_count=Count('id', filter=Q(status='IN')),
        out_count=Count('id', filter=Q(status='OUT'))
    ).order_by('-total')[:10]
    
    # Peak hours analysis
    peak_hours = visitors.filter(
        entry_time__gte=week_start
    ).annotate(
        hour=TruncHour('entry_time')
    ).values('hour').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Daily trend (last 7 days)
    daily_trend = visitors.filter(
        entry_time__gte=week_start
    ).annotate(
        date=TruncDate('entry_time')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')
    
    context = {
        'total_today': visitors.filter(entry_time__gte=today_start).count(),
        'total_week': visitors.filter(entry_time__gte=week_start).count(),
        'total_month': visitors.filter(entry_time__gte=month_start).count(),
        'dept_stats': dept_stats,
        'peak_hours': peak_hours,
        'daily_trend': daily_trend,
    }
    
    return render(request, 'visitors/analytics.html', context)


@login_required
def generate_report(request):
    report_type = request.GET.get('type', 'daily')
    visitors = Visitor.objects.filter(created_by=request.user)
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    if report_type == 'daily':
        visitors = visitors.filter(entry_time__gte=today_start)
        title = f"Daily Report - {today_start.strftime('%d %b %Y')}"
    elif report_type == 'weekly':
        week_start = today_start - timedelta(days=7)
        visitors = visitors.filter(entry_time__gte=week_start)
        title = f"Weekly Report - Last 7 Days"
    elif report_type == 'monthly':
        month_start = today_start - timedelta(days=30)
        visitors = visitors.filter(entry_time__gte=month_start)
        title = f"Monthly Report - Last 30 Days"
    else:
        title = "All Visitors Report"
    
    visitors = visitors.order_by('-entry_time')
    
    context = {
        'visitors': visitors,
        'title': title,
        'report_type': report_type,
        'total': visitors.count(),
        'in_count': visitors.filter(status='IN').count(),
        'out_count': visitors.filter(status='OUT').count(),
    }
    
    return render(request, 'visitors/report.html', context)


@login_required
def export_csv(request):
    report_type = request.GET.get('type', 'daily')
    visitors = Visitor.objects.filter(created_by=request.user)
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    if report_type == 'daily':
        visitors = visitors.filter(entry_time__gte=today_start)
        filename = f"daily_report_{today_start.strftime('%Y%m%d')}.csv"
    elif report_type == 'weekly':
        week_start = today_start - timedelta(days=7)
        visitors = visitors.filter(entry_time__gte=week_start)
        filename = "weekly_report.csv"
    elif report_type == 'monthly':
        month_start = today_start - timedelta(days=30)
        visitors = visitors.filter(entry_time__gte=month_start)
        filename = "monthly_report.csv"
    else:
        filename = "all_visitors.csv"
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Mobile', 'Email', 'Purpose', 'Visit To', 'Department', 'Entry Time', 'Exit Time', 'Status'])
    
    for v in visitors:
        writer.writerow([
            v.name, v.mobile, v.email, v.purpose, v.visit_to,
            v.hostel_or_office, v.entry_time.strftime('%Y-%m-%d %H:%M'),
            v.exit_time.strftime('%Y-%m-%d %H:%M') if v.exit_time else 'N/A',
            v.status
        ])
    
    return response


# =========================
# Send Checkout Reminders
# =========================
@login_required
def send_reminders(request):
    """Send checkout reminders to long-staying visitors"""
    from .notifications import send_checkout_reminder_email, send_checkout_reminder_sms
    
    now = timezone.now()
    long_staying = Visitor.objects.filter(
        status='IN',
        entry_time__lt=now - timedelta(hours=4)
    )
    
    count = 0
    for visitor in long_staying:
        send_checkout_reminder_email(visitor)
        send_checkout_reminder_sms(visitor)
        count += 1
    
    messages.success(request, f"Sent reminders to {count} visitor(s)")
    return redirect('dashboard')
