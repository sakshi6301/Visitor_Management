# 📊 Reports & Analytics - Complete Guide

## ✅ Features Implemented

### 1. **Analytics Dashboard**
- **URL**: `/analytics/`
- **Features**:
  - Summary cards (Today, Week, Month)
  - Department-wise visitor analysis
  - Peak visiting hours (last 7 days)
  - Daily trend visualization
  - Quick report generation buttons

### 2. **Report Generation**
- **Daily Report**: Today's visitors
- **Weekly Report**: Last 7 days
- **Monthly Report**: Last 30 days
- **All Time Report**: Complete history

### 3. **Department-wise Analysis**
- Total visitors per department
- IN/OUT status breakdown
- Top 10 departments by visitor count

### 4. **Peak Hours Analysis**
- Hourly visitor distribution
- Visual progress bars
- Last 7 days data
- Top 10 busiest hours

### 5. **Export Options**
- **CSV Export**: Download reports as Excel-compatible CSV
- **PDF Export**: Print to PDF using browser print function
- Includes all visitor details

---

## 🚀 How to Use

### Access Analytics Dashboard
```
1. Login to system
2. Click "📊 Analytics" in sidebar
3. View all analytics and trends
```

### Generate Reports

#### Option 1: From Analytics Page
```
1. Go to Analytics Dashboard
2. Click report button:
   - Daily Report
   - Weekly Report
   - Monthly Report
   - All Time
```

#### Option 2: From Sidebar
```
1. Click "📄 Reports" in sidebar
2. Select report type from buttons
```

#### Option 3: Direct URL
```
Daily:   /reports/generate/?type=daily
Weekly:  /reports/generate/?type=weekly
Monthly: /reports/generate/?type=monthly
All:     /reports/generate/?type=all
```

### Export to CSV
```
1. Open any report
2. Click "📥 Export CSV" button
3. File downloads automatically
4. Open in Excel/Google Sheets
```

### Export to PDF
```
1. Open any report
2. Click "🖨️ Print PDF" button
3. Select "Save as PDF" in print dialog
4. Choose location and save
```

---

## 📋 Report Contents

### CSV Export Includes:
- Name
- Mobile
- Email
- Purpose
- Visit To (Person)
- Department (Hostel/Office)
- Entry Time
- Exit Time
- Status (IN/OUT)

### Report Table Shows:
- All above fields
- Visit duration
- Sequential numbering
- Color-coded status badges

---

## 📊 Analytics Metrics

### Summary Cards
- **Today's Visitors**: Count from midnight today
- **This Week**: Last 7 days
- **This Month**: Last 30 days

### Department Analysis
Shows for each department:
- Total visitors
- Currently IN
- Checked OUT
- Sorted by total (highest first)
- Top 10 departments displayed

### Peak Hours
- Hourly breakdown of visits
- Visual progress bars
- Based on last 7 days
- Shows date, hour, and count
- Top 10 busiest hours

### Daily Trend
- Day-by-day visitor count
- Last 7 days
- Visual progress bars
- Helps identify patterns

---

## 🎯 Use Cases

### For Management
```
- Monthly reports for board meetings
- Department-wise visitor analysis
- Peak hours for staff planning
- Trend analysis for capacity planning
```

### For Security
```
- Daily reports for shift handover
- Real-time IN/OUT status
- Department-wise monitoring
- Export for record keeping
```

### For Administration
```
- Weekly summaries
- Visitor pattern analysis
- Resource allocation based on peak hours
- Historical data for audits
```

---

## 🔧 Technical Details

### New Views Added
```python
analytics_dashboard(request)  # Main analytics page
generate_report(request)       # Report generation
export_csv(request)            # CSV export
```

### Database Queries Used
```python
# Department-wise aggregation
.values('hostel_or_office').annotate(total=Count('id'))

# Peak hours analysis
.annotate(hour=TruncHour('entry_time')).values('hour')

# Daily trend
.annotate(date=TruncDate('entry_time')).values('date')
```

### URL Routes
```
/analytics/                  - Analytics dashboard
/reports/generate/           - Generate reports
/reports/export-csv/         - Export CSV
```

---

## 📱 Mobile Responsive

All reports and analytics are mobile-friendly:
- Tables scroll horizontally on small screens
- Cards stack vertically
- Buttons adapt to screen size
- Print/Export works on mobile browsers

---

## 🎨 Customization

### Change Report Period

**In views.py:**
```python
# Change weekly from 7 to 14 days
week_start = today_start - timedelta(days=14)

# Change monthly from 30 to 60 days
month_start = today_start - timedelta(days=60)
```

### Change Top N Departments

**In views.py (analytics_dashboard):**
```python
# Change from top 10 to top 5
).order_by('-total')[:5]
```

### Change Peak Hours Count

**In views.py (analytics_dashboard):**
```python
# Change from 10 to 20 hours
).order_by('-count')[:20]
```

### Customize CSV Columns

**In views.py (export_csv):**
```python
# Add/remove columns in writerow
writer.writerow(['Name', 'Mobile', 'Custom Field'])
```

---

## 📈 Sample Outputs

### CSV Export Format
```csv
Name,Mobile,Email,Purpose,Visit To,Department,Entry Time,Exit Time,Status
John Doe,9876543210,john@email.com,Meeting,Mr. Smith,Admin Office,2024-01-15 10:30,2024-01-15 12:00,OUT
Jane Smith,9876543211,jane@email.com,Delivery,Reception,Main Gate,2024-01-15 11:00,N/A,IN
```

### Analytics Dashboard Shows
```
Today's Visitors: 15
This Week: 87
This Month: 342

Top Departments:
1. Admin Office - 45 visitors
2. HR Department - 32 visitors
3. IT Department - 28 visitors

Peak Hours:
1. 15 Jan, 10 AM - 12 visitors
2. 15 Jan, 2 PM - 10 visitors
3. 14 Jan, 11 AM - 9 visitors
```

---

## 🔍 Filtering & Sorting

### Current Implementation
- Reports filtered by date range
- Sorted by entry time (newest first)
- Department stats sorted by total count
- Peak hours sorted by visitor count

### Future Enhancements
- Filter by department
- Filter by status (IN/OUT)
- Date range picker
- Search within reports

---

## 💡 Tips & Best Practices

### For Accurate Reports
1. Ensure all visitors are checked out
2. Run reports at end of day
3. Export regularly for backup
4. Compare trends week-over-week

### For Better Analytics
1. Encourage staff to use correct department names
2. Check peak hours for staffing needs
3. Monitor long-staying visitors
4. Review monthly trends for planning

### For Data Management
1. Export monthly reports for archives
2. Keep CSV backups
3. Print important reports to PDF
4. Share analytics with management

---

## 🐛 Troubleshooting

### No Data in Analytics
- Check if visitors exist for selected period
- Verify you're logged in
- Ensure visitors belong to your account

### CSV Download Not Working
- Check browser download settings
- Try different browser
- Verify file permissions

### Print PDF Issues
- Use Chrome/Edge for best results
- Check print preview before saving
- Adjust page orientation if needed

### Empty Department Stats
- Visitors need hostel_or_office field filled
- Check data entry completeness

---

## 📞 Quick Reference

### URLs
```
Analytics:     /analytics/
Daily Report:  /reports/generate/?type=daily
Weekly:        /reports/generate/?type=weekly
Monthly:       /reports/generate/?type=monthly
Export CSV:    /reports/export-csv/?type=daily
```

### Sidebar Navigation
```
📊 Analytics  → Analytics Dashboard
📄 Reports    → Daily Report (default)
```

### Export Shortcuts
```
CSV:  Click "📥 Export CSV" button
PDF:  Click "🖨️ Print PDF" button or Ctrl+P
```

---

## ✨ Summary

**What You Can Do Now:**
✅ View comprehensive analytics dashboard  
✅ Generate daily/weekly/monthly reports  
✅ Analyze department-wise visitor data  
✅ Identify peak visiting hours  
✅ Export reports to CSV (Excel)  
✅ Print reports to PDF  
✅ Track visitor trends over time  
✅ Make data-driven decisions  

**All features are production-ready and fully functional!** 🎉

---

**Version**: 3.0  
**Module**: Reports & Analytics  
**Status**: ✅ Complete
