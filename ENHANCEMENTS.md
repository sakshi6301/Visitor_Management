# Visitor Management System - Enhancements

## 🚀 New Features Implemented

### 1. **Notifications & Alerts**

#### Long-Staying Visitor Alerts
- **Dashboard Alert**: Automatic warning banner appears when visitors stay longer than 4 hours
- **Real-time Detection**: System checks entry time vs current time
- **Visual Indicator**: Yellow warning banner with visitor count
- **Auto-reload**: Dashboard refreshes when long-staying visitors detected

#### Daily Summary Reports
- **Management Command**: Run `python manage.py daily_summary` to generate reports
- **API Endpoint**: `/api/daily-summary/` returns JSON summary
- **Metrics Included**:
  - Total visitors for the day
  - Currently IN count
  - Checked OUT count
  - Long-staying visitors (>4 hours)
- **Usage**: Can be scheduled with cron jobs or Task Scheduler

---

### 2. **Better UI/UX**

#### Pagination
- **Visitor List**: 10 visitors per page with navigation controls
- **Employee List**: 10 employees per page
- **Navigation**: First, Previous, Next, Last buttons
- **Page Counter**: Shows current page and total pages

#### Auto-Refresh Dashboard
- **Interval**: Updates every 30 seconds automatically
- **API Endpoint**: `/api/dashboard-stats/` provides real-time data
- **Updated Stats**:
  - Today's visitors
  - Yesterday's visitors
  - Last 7 days visitors
  - Total visitors
  - Long-staying count
- **No Page Reload**: Uses AJAX for seamless updates

#### Mobile-Responsive Design
- **Viewport Meta Tag**: Added for proper mobile scaling
- **Responsive CSS**: Media queries for screens < 768px
- **Adaptive Layout**:
  - Sidebar collapses on mobile
  - Tables become scrollable
  - Buttons stack vertically
  - Font sizes adjust
  - Topbar becomes vertical

#### Recent Visitors Widget
- **Dashboard Addition**: Shows last 5 visitors
- **Quick View**: Name, mobile, purpose, entry time, status
- **Real-time**: Updates with dashboard refresh

---

## 📋 How to Use

### Running Daily Summary Report

**Option 1: Manual Command**
```bash
python manage.py daily_summary
```

**Option 2: Schedule with Windows Task Scheduler**
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 11:59 PM
4. Action: Start a program
5. Program: `python`
6. Arguments: `manage.py daily_summary`
7. Start in: `c:\Users\Sneha Hudge\Downloads\VisitorManagementSystem\VisitorManagementSystem\visitor_management`

**Option 3: Use API Endpoint**
```javascript
fetch('/api/daily-summary/')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Testing Auto-Refresh Dashboard
1. Open dashboard in browser
2. Add a new visitor in another tab
3. Wait 30 seconds
4. Dashboard stats will update automatically

### Testing Long-Staying Alerts
1. Manually adjust a visitor's entry_time in database to 5 hours ago
2. Refresh dashboard
3. Yellow alert banner will appear

### Testing Pagination
1. Add more than 10 visitors
2. Navigate to visitor list
3. Pagination controls appear at bottom

---

## 🔧 Technical Details

### New API Endpoints

**1. Dashboard Stats API**
- **URL**: `/api/dashboard-stats/`
- **Method**: GET
- **Auth**: Login required
- **Response**:
```json
{
  "total_today": 5,
  "total_yesterday": 3,
  "total_last_7_days": 15,
  "total_visitors": 50,
  "long_staying_count": 2
}
```

**2. Daily Summary API**
- **URL**: `/api/daily-summary/`
- **Method**: GET
- **Auth**: Login required
- **Response**:
```json
{
  "date": "2024-01-15",
  "total_visitors": 5,
  "currently_in": 2,
  "checked_out": 3,
  "long_staying": 1
}
```

### Modified Files

**Backend:**
- `visitors/views.py` - Added pagination, alerts, API endpoints
- `visitors/urls.py` - Added new API routes
- `visitors/models.py` - No changes (existing models sufficient)

**Frontend:**
- `templates/visitors/dashboard.html` - Alert banner, recent visitors, auto-refresh
- `templates/visitors/visitor_list.html` - Pagination controls, mobile viewport
- `templates/visitors/employee_list.html` - Pagination controls
- `templates/visitors/base.html` - Mobile-responsive CSS

**Management:**
- `visitors/management/commands/daily_summary.py` - Daily report command

---

## 📱 Mobile Responsive Features

### Breakpoint: 768px

**Changes on Mobile:**
- Content area: No left margin, full width
- Topbar: Vertical layout with stacked elements
- Stat cards: Full width with bottom margin
- Tables: Smaller font (0.85rem), horizontal scroll
- Sidebar: Full width, relative positioning
- Buttons: Stack vertically, full width

### Testing Mobile View
1. Open browser DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Select mobile device (iPhone, Android)
4. Navigate through pages

---

## ⚙️ Configuration Options

### Adjust Long-Staying Threshold
In `visitors/views.py`, change the timedelta:
```python
# Current: 4 hours
entry_time__lt=now - timedelta(hours=4)

# Change to 2 hours:
entry_time__lt=now - timedelta(hours=2)
```

### Adjust Auto-Refresh Interval
In `templates/visitors/dashboard.html`, change the interval:
```javascript
// Current: 30 seconds (30000 ms)
}, 30000);

// Change to 1 minute:
}, 60000);
```

### Adjust Pagination Size
In `visitors/views.py`, change the paginator:
```python
# Current: 10 per page
paginator = Paginator(visitors, 10)

# Change to 20 per page:
paginator = Paginator(visitors, 20)
```

---

## 🎯 Benefits

1. **Improved Security**: Alerts for visitors overstaying
2. **Better Performance**: Pagination reduces page load time
3. **Real-time Monitoring**: Auto-refresh keeps data current
4. **Mobile Access**: Staff can use phones/tablets
5. **Reporting**: Daily summaries for management review
6. **User Experience**: Smoother navigation, faster responses

---

## 🔮 Future Enhancement Ideas

- Email notifications for long-staying visitors
- SMS alerts for security staff
- Export daily summary to PDF/Excel
- Visitor check-in via QR code
- Biometric integration
- Visitor pre-registration portal
- Analytics dashboard with charts

---

## 📞 Support

For issues or questions:
1. Check browser console for JavaScript errors
2. Check Django logs for backend errors
3. Verify database migrations are applied
4. Test API endpoints directly in browser

---

**Version**: 2.0  
**Last Updated**: 2024  
**Status**: Production Ready ✅
