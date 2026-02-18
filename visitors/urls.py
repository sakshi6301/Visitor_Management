from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('register/', views.register_view, name='register'),  # Disabled for receptionist-only

    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/dashboard-stats/', views.dashboard_stats, name='dashboard_stats'),
    path('api/daily-summary/', views.daily_summary, name='daily_summary'),

    # ===== EMPLOYEE =====
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path("employee/checkin/<int:emp_id>/", views.employee_checkin, name="employee_checkin"),
    path("employee/checkout/<int:emp_id>/", views.employee_checkout, name="employee_checkout"),


    # ===== VISITOR =====
    path('visitors/', views.visitor_list, name='visitor_list'),
    path('add/', views.add_visitor, name='add_visitor'),
    path('checkout/<int:visitor_id>/', views.checkout_visitor, name='checkout_visitor'),
    path('report/', views.visitor_report, name='visitor_report'),

    # ===== ANALYTICS & REPORTS =====
    path('analytics/', views.analytics_dashboard, name='analytics'),
    path('reports/generate/', views.generate_report, name='generate_report'),
    path('reports/export-csv/', views.export_csv, name='export_csv'),

    # ===== NOTIFICATIONS =====
    path('send-reminders/', views.send_reminders, name='send_reminders'),

    path('profile/', views.profile, name='profile'),
]
