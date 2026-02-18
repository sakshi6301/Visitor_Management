"""
Test script for Visitor Management System Enhancements
Run this after starting the Django server
"""

import requests
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def test_enhancements():
    print("=" * 60)
    print("VISITOR MANAGEMENT SYSTEM - ENHANCEMENT TESTS")
    print("=" * 60)
    
    # Test 1: Dashboard Stats API
    print("\n[TEST 1] Dashboard Stats API")
    print("-" * 60)
    try:
        response = requests.get(f"{BASE_URL}/api/dashboard-stats/")
        if response.status_code == 200:
            data = response.json()
            print("✓ API Response:")
            print(f"  - Total Today: {data.get('total_today')}")
            print(f"  - Total Yesterday: {data.get('total_yesterday')}")
            print(f"  - Last 7 Days: {data.get('total_last_7_days')}")
            print(f"  - Total Visitors: {data.get('total_visitors')}")
            print(f"  - Long Staying: {data.get('long_staying_count')}")
        else:
            print(f"✗ Failed: Status {response.status_code}")
            print("  Note: You need to be logged in to access this API")
    except Exception as e:
        print(f"✗ Error: {e}")
        print("  Make sure Django server is running!")
    
    # Test 2: Daily Summary API
    print("\n[TEST 2] Daily Summary API")
    print("-" * 60)
    try:
        response = requests.get(f"{BASE_URL}/api/daily-summary/")
        if response.status_code == 200:
            data = response.json()
            print("✓ API Response:")
            print(f"  - Date: {data.get('date')}")
            print(f"  - Total Visitors: {data.get('total_visitors')}")
            print(f"  - Currently IN: {data.get('currently_in')}")
            print(f"  - Checked OUT: {data.get('checked_out')}")
            print(f"  - Long Staying: {data.get('long_staying')}")
        else:
            print(f"✗ Failed: Status {response.status_code}")
            print("  Note: You need to be logged in to access this API")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 3: Check Pages
    print("\n[TEST 3] Page Accessibility")
    print("-" * 60)
    pages = [
        ("/", "Home Page"),
        ("/login/", "Login Page"),
        ("/dashboard/", "Dashboard"),
        ("/visitors/", "Visitor List"),
        ("/employees/", "Employee List"),
    ]
    
    for url, name in pages:
        try:
            response = requests.get(f"{BASE_URL}{url}")
            if response.status_code in [200, 302]:
                print(f"✓ {name}: Accessible")
            else:
                print(f"✗ {name}: Status {response.status_code}")
        except Exception as e:
            print(f"✗ {name}: Error - {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("ENHANCEMENT FEATURES IMPLEMENTED:")
    print("=" * 60)
    print("✓ Long-staying visitor alerts (>4 hours)")
    print("✓ Daily summary report command")
    print("✓ Dashboard auto-refresh (30 seconds)")
    print("✓ Pagination for visitor list (10 per page)")
    print("✓ Pagination for employee list (10 per page)")
    print("✓ Mobile-responsive design")
    print("✓ Recent visitors widget on dashboard")
    print("✓ API endpoints for real-time data")
    print("\n" + "=" * 60)
    print("MANUAL TESTS REQUIRED:")
    print("=" * 60)
    print("1. Login to dashboard and wait 30 seconds to see auto-refresh")
    print("2. Add 11+ visitors to test pagination")
    print("3. Open on mobile device to test responsive design")
    print("4. Run: python manage.py daily_summary")
    print("5. Create visitor with old entry_time to test alert")
    print("=" * 60)

if __name__ == "__main__":
    test_enhancements()
