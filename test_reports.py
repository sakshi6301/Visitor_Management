"""
Quick Test Script for Reports & Analytics Module
Run after starting Django server
"""

print("=" * 70)
print("REPORTS & ANALYTICS - FEATURE TEST CHECKLIST")
print("=" * 70)

print("\n✅ FEATURES IMPLEMENTED:\n")

features = [
    "📊 Analytics Dashboard with summary cards",
    "📈 Department-wise visitor analysis",
    "⏰ Peak visiting hours identification",
    "📅 Daily trend visualization (last 7 days)",
    "📄 Daily Report generation",
    "📄 Weekly Report generation (last 7 days)",
    "📄 Monthly Report generation (last 30 days)",
    "📄 All-time Report generation",
    "📥 CSV Export functionality",
    "🖨️ PDF Export (via print)",
    "📊 Visual progress bars for trends",
    "🎨 Mobile-responsive design",
]

for i, feature in enumerate(features, 1):
    print(f"{i:2}. {feature}")

print("\n" + "=" * 70)
print("MANUAL TESTING STEPS")
print("=" * 70)

tests = [
    ("Analytics Dashboard", [
        "1. Navigate to /analytics/",
        "2. Verify summary cards show correct counts",
        "3. Check department-wise table",
        "4. Verify peak hours display",
        "5. Check daily trend chart"
    ]),
    ("Report Generation", [
        "1. Click 'Daily Report' button",
        "2. Verify correct data displayed",
        "3. Try Weekly, Monthly, All Time",
        "4. Check report type highlighting"
    ]),
    ("CSV Export", [
        "1. Open any report",
        "2. Click 'Export CSV' button",
        "3. Verify file downloads",
        "4. Open in Excel/Sheets",
        "5. Check all columns present"
    ]),
    ("PDF Export", [
        "1. Open any report",
        "2. Click 'Print PDF' button",
        "3. Select 'Save as PDF'",
        "4. Verify formatting",
        "5. Check no buttons in PDF"
    ]),
    ("Mobile View", [
        "1. Open DevTools (F12)",
        "2. Toggle device mode",
        "3. Test analytics page",
        "4. Test reports page",
        "5. Verify tables scroll"
    ]),
]

for test_name, steps in tests:
    print(f"\n📋 {test_name}:")
    for step in steps:
        print(f"   {step}")

print("\n" + "=" * 70)
print("URL QUICK REFERENCE")
print("=" * 70)

urls = {
    "Analytics Dashboard": "http://127.0.0.1:8000/analytics/",
    "Daily Report": "http://127.0.0.1:8000/reports/generate/?type=daily",
    "Weekly Report": "http://127.0.0.1:8000/reports/generate/?type=weekly",
    "Monthly Report": "http://127.0.0.1:8000/reports/generate/?type=monthly",
    "All Time Report": "http://127.0.0.1:8000/reports/generate/?type=all",
    "Export CSV (Daily)": "http://127.0.0.1:8000/reports/export-csv/?type=daily",
}

for name, url in urls.items():
    print(f"\n{name}:")
    print(f"  {url}")

print("\n" + "=" * 70)
print("EXPECTED RESULTS")
print("=" * 70)

print("""
✓ Analytics page shows 3 summary cards
✓ Department table shows top 10 departments
✓ Peak hours shows top 10 busiest times
✓ Daily trend shows last 7 days
✓ Reports show all visitor details
✓ CSV downloads with proper filename
✓ PDF prints without buttons/sidebar
✓ All pages are mobile-responsive
✓ Sidebar has Analytics and Reports links
""")

print("=" * 70)
print("SAMPLE DATA NEEDED FOR TESTING")
print("=" * 70)

print("""
To properly test all features, ensure you have:
- At least 10 visitors in the system
- Visitors from different departments
- Visitors from different days (last 7 days)
- Some visitors with IN status
- Some visitors with OUT status
- Visitors at different hours of the day
""")

print("\n" + "=" * 70)
print("START TESTING NOW!")
print("=" * 70)
print("\n1. Start server: python manage.py runserver")
print("2. Login to system")
print("3. Click 'Analytics' in sidebar")
print("4. Follow test steps above")
print("\n" + "=" * 70)
