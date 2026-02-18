from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


# =========================
# Email Notifications
# =========================

def send_host_notification_email(visitor, host_email):
    """Send email to host when visitor arrives"""
    subject = f"Visitor Arrival: {visitor.name}"
    message = f"""
    Dear {visitor.visit_to},
    
    A visitor has arrived to meet you:
    
    Name: {visitor.name}
    Mobile: {visitor.mobile}
    Purpose: {visitor.purpose}
    Entry Time: {visitor.entry_time.strftime('%d %b %Y, %I:%M %p')}
    
    Please proceed to reception.
    
    Regards,
    Visitor Management System
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [host_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


def send_visitor_confirmation_email(visitor):
    """Send confirmation email to visitor"""
    subject = "Visit Confirmation - Entry Registered"
    message = f"""
    Dear {visitor.name},
    
    Your visit has been registered successfully.
    
    Details:
    - Visiting: {visitor.visit_to}
    - Department: {visitor.hostel_or_office}
    - Purpose: {visitor.purpose}
    - Entry Time: {visitor.entry_time.strftime('%d %b %Y, %I:%M %p')}
    
    Thank you for visiting us!
    
    Regards,
    Visitor Management System
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [visitor.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


def send_checkout_reminder_email(visitor):
    """Send checkout reminder to visitor"""
    subject = "Checkout Reminder"
    message = f"""
    Dear {visitor.name},
    
    This is a reminder to check out before leaving.
    
    Entry Time: {visitor.entry_time.strftime('%d %b %Y, %I:%M %p')}
    Duration: {(timezone.now() - visitor.entry_time).seconds // 3600} hours
    
    Please visit reception to complete checkout.
    
    Regards,
    Visitor Management System
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [visitor.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


# =========================
# SMS Notifications
# =========================

def send_host_notification_sms(visitor, host_mobile):
    """Send SMS to host when visitor arrives"""
    message = f"Visitor Alert: {visitor.name} ({visitor.mobile}) has arrived to meet you. Purpose: {visitor.purpose}. Time: {visitor.entry_time.strftime('%I:%M %p')}"
    
    try:
        from twilio.rest import Client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        msg = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=host_mobile
        )
        print(f"✓ SMS sent to {host_mobile}: SID={msg.sid}")
        return True
    except Exception as e:
        print(f"✗ SMS error: {e}")
        return False


def send_visitor_confirmation_sms(visitor):
    """Send confirmation SMS to visitor"""
    message = f"Visit registered! Visiting: {visitor.visit_to}, Dept: {visitor.hostel_or_office}. Entry: {visitor.entry_time.strftime('%I:%M %p')}. Thank you!"
    
    try:
        from twilio.rest import Client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        msg = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=visitor.mobile
        )
        print(f"✓ SMS sent to {visitor.mobile}: SID={msg.sid}")
        return True
    except Exception as e:
        print(f"✗ SMS error: {e}")
        return False


def send_checkout_reminder_sms(visitor):
    """Send checkout reminder SMS"""
    hours = (timezone.now() - visitor.entry_time).seconds // 3600
    message = f"Reminder: Please check out before leaving. You've been here for {hours} hours. Visit reception. Thank you!"
    
    try:
        from twilio.rest import Client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        msg = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=visitor.mobile
        )
        print(f"✓ SMS sent to {visitor.mobile}: SID={msg.sid}")
        return True
    except Exception as e:
        print(f"✗ SMS error: {e}")
        return False
