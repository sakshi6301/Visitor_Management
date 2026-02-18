from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from visitors.models import Visitor
from visitors.notifications import send_checkout_reminder_email, send_checkout_reminder_sms


class Command(BaseCommand):
    help = 'Send checkout reminders to long-staying visitors'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        
        # Find visitors who have been inside for more than 4 hours
        long_staying = Visitor.objects.filter(
            status='IN',
            entry_time__lt=now - timedelta(hours=4)
        )
        
        count = 0
        for visitor in long_staying:
            # Send email reminder
            email_sent = send_checkout_reminder_email(visitor)
            
            # Send SMS reminder
            sms_sent = send_checkout_reminder_sms(visitor)
            
            if email_sent or sms_sent:
                count += 1
                self.stdout.write(f"Reminder sent to: {visitor.name} ({visitor.mobile})")
        
        if count > 0:
            self.stdout.write(self.style.SUCCESS(f'\n✓ Sent reminders to {count} visitor(s)\n'))
        else:
            self.stdout.write(self.style.WARNING('\nNo long-staying visitors found\n'))
