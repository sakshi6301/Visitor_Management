from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Visitor(models.Model):

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    STATUS_CHOICES = (
        ('IN', 'IN'),
        ('OUT', 'OUT'),
    )

    # =====================
    # USER (PROFILE LINK)
    # =====================
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='visitors'
    )

    # =====================
    # BASIC INFO
    # =====================
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    email = models.EmailField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    # =====================
    # VISIT INFO
    # =====================
    purpose = models.CharField(max_length=200)
    visit_to = models.CharField(max_length=100)

    # 🔥 SINGLE FIELD
    hostel_or_office = models.CharField(max_length=200)

    address = models.TextField()

    # =====================
    # AADHAAR
    # =====================
    aadhaar = models.CharField(max_length=12)

    # =====================
    # MEDIA
    # =====================
    photo = models.ImageField(upload_to='visitor_photos/', null=True, blank=True)
    signature = models.ImageField(upload_to='signatures/')

    # =====================
    # STATUS
    # =====================
    status = models.CharField(
        max_length=5,
        choices=STATUS_CHOICES,
        default='IN'
    )

    entry_time = models.DateTimeField(default=timezone.now)
    exit_time = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # =====================
    # DISPLAY
    # =====================
    def __str__(self):
        return f"{self.name} - {self.mobile}"

    def masked_aadhaar(self):
        if len(self.aadhaar) == 12:
            return "XXXX-XXXX-" + self.aadhaar[-4:]
        return ""


# =========================
# Employee / Staff Model
# =========================

class Employee(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    work_as = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    signature = models.ImageField(
        upload_to='employee_sign/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(default=timezone.now)  # 🔥 TEMP FIX

    def __str__(self):
        return self.name


# =========================
# Employee Attendance
# =========================
class EmployeeAttendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    in_time = models.TimeField(null=True, blank=True)
    out_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Present')

    def __str__(self):
        return f"{self.employee.name} - {self.date}"
