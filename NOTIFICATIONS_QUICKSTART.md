# 🔔 NOTIFICATIONS - Quick Setup Guide

## ✅ What's Been Implemented

### Email Notifications:
✅ Host notification on visitor arrival  
✅ Visitor confirmation email  
✅ Checkout reminder email  

### SMS Notifications:
✅ Host SMS on visitor arrival  
✅ Visitor confirmation SMS  
✅ Checkout reminder SMS  

### Automation:
✅ Management command for scheduled reminders  
✅ Manual reminder trigger  
✅ Long-staying visitor detection (>4 hours)  

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Configure Email (Gmail)

**1. Get App Password:**
```
1. Go to: https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Go to: App passwords
4. Select "Mail" → "Other" → Name it "Visitor System"
5. Copy the 16-character password
```

**2. Update settings.py:**
```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-16-char-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

**3. Test:**
```bash
python manage.py shell
```
```python
from django.core.mail import send_mail
send_mail('Test', 'Working!', 'your-email@gmail.com', ['test@example.com'])
```

### Step 2: Configure SMS (Optional - Twilio)

**1. Sign up:**
- Go to: https://www.twilio.com/
- Create free trial account
- Get phone number

**2. Get credentials:**
- Dashboard → Account SID
- Dashboard → Auth Token

**3. Install Twilio:**
```bash
pip install twilio
```

**4. Update settings.py:**
```python
TWILIO_ACCOUNT_SID = 'your-sid'
TWILIO_AUTH_TOKEN = 'your-token'
TWILIO_PHONE_NUMBER = '+1234567890'
```

**5. Uncomment code in notifications.py:**
- Find all Twilio code blocks
- Remove the comment marks (#)

---

## 📋 How It Works

### When Adding Visitor:

**Form Fields:**
```
✓ Visitor details (name, mobile, email, etc.)
✓ Host Email (optional) → Sends email to host
✓ Host Mobile (optional) → Sends SMS to host
```

**What Happens:**
```
1. Visitor record created
2. Host notification sent (if email/mobile provided)
3. Visitor confirmation sent
4. Success message displayed
```

### Checkout Reminders:

**Manual Trigger:**
```
Navigate to: /send-reminders/
Sends reminders to all visitors IN > 4 hours
```

**Automated (Schedule):**
```bash
# Run command
python manage.py send_checkout_reminders

# Schedule with Task Scheduler (Windows)
- Daily at 5 PM
- Program: python
- Arguments: manage.py send_checkout_reminders
```

---

## 📧 Notification Examples

### Host Email:
```
Subject: Visitor Arrival: John Doe

Dear Mr. Smith,

A visitor has arrived to meet you:

Name: John Doe
Mobile: 9876543210
Purpose: Meeting
Entry Time: 15 Jan 2024, 10:30 AM

Please proceed to reception.
```

### Visitor Email:
```
Subject: Visit Confirmation - Entry Registered

Dear John Doe,

Your visit has been registered successfully.

Details:
- Visiting: Mr. Smith
- Department: Admin Office
- Purpose: Meeting
- Entry Time: 15 Jan 2024, 10:30 AM

Thank you for visiting us!
```

### Reminder Email:
```
Subject: Checkout Reminder

Dear John Doe,

This is a reminder to check out before leaving.

Entry Time: 15 Jan 2024, 10:30 AM
Duration: 5 hours

Please visit reception to complete checkout.
```

---

## 🧪 Testing Checklist

### ✅ Email Testing:
- [ ] Configure Gmail App Password
- [ ] Update settings.py
- [ ] Test with shell command
- [ ] Add visitor with host email
- [ ] Check host receives email
- [ ] Check visitor receives email

### ✅ SMS Testing (Optional):
- [ ] Sign up for Twilio
- [ ] Get credentials
- [ ] Install twilio package
- [ ] Uncomment code in notifications.py
- [ ] Add visitor with host mobile
- [ ] Check SMS received

### ✅ Reminder Testing:
- [ ] Create visitor with old entry_time
- [ ] Run: python manage.py send_checkout_reminders
- [ ] Check email/SMS received
- [ ] Test manual trigger: /send-reminders/

---

## 📁 Files Reference

### Configuration:
```
visitor_management/settings.py    - Email/SMS config
```

### Notification Logic:
```
visitors/notifications.py         - All notification functions
```

### Views:
```
visitors/views.py                 - add_visitor (sends notifications)
                                  - send_reminders (manual trigger)
```

### Templates:
```
visitors/templates/visitors/visitor_entry.html  - Host contact fields
```

### Commands:
```
visitors/management/commands/send_checkout_reminders.py
```

---

## 🔧 Customization

### Change Reminder Time:
```python
# In notifications.py and views.py
# Change from 4 hours to 2 hours
entry_time__lt=now - timedelta(hours=2)
```

### Customize Email Content:
```python
# In notifications.py
def send_host_notification_email(visitor, host_email):
    subject = "Your Custom Subject"
    message = "Your custom message..."
```

### Add More Notifications:
```python
# Example: Checkout confirmation
def send_checkout_confirmation(visitor):
    subject = "Thank You for Visiting"
    message = f"Thank you {visitor.name}..."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [visitor.email])
```

---

## 🐛 Common Issues

### Email not sending?
```
✓ Check App Password (not regular password)
✓ Enable 2FA first
✓ Check firewall/antivirus
✓ Verify EMAIL_HOST_USER matches DEFAULT_FROM_EMAIL
```

### SMS not working?
```
✓ Verify Twilio credentials
✓ Check phone number format (+country code)
✓ Verify recipient number (trial mode)
✓ Uncomment Twilio code in notifications.py
```

### Reminders not triggered?
```
✓ Check visitor status = 'IN'
✓ Verify entry_time > 4 hours ago
✓ Run command manually first
✓ Check email/SMS configuration
```

---

## 💡 Pro Tips

1. **Test First**: Always test with your own email/phone
2. **Monitor Logs**: Check console for error messages
3. **Start Simple**: Get email working first, then add SMS
4. **Schedule Smart**: Run reminders during business hours
5. **Keep Messages Short**: Especially for SMS (160 chars)

---

## 📞 Quick Commands

### Test Email:
```bash
python manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'Message', 'from@email.com', ['to@email.com'])
```

### Send Reminders:
```bash
python manage.py send_checkout_reminders
```

### Manual Trigger:
```
Navigate to: http://127.0.0.1:8000/send-reminders/
```

---

## 🎉 You're Ready!

**What Works Now:**
✅ Email notifications on visitor arrival  
✅ Visitor confirmation emails  
✅ Checkout reminder emails  
✅ SMS notifications (when configured)  
✅ Automated reminder system  
✅ Manual reminder trigger  

**Next Steps:**
1. Configure email (5 minutes)
2. Test with real visitor
3. Optionally setup SMS
4. Schedule automated reminders

---

**Version**: 4.0  
**Status**: ✅ PRODUCTION READY  

🚀 **Start sending notifications now!** 🚀
