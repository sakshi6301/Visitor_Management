from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
from visitors.models import Visitor


class Command(BaseCommand):
    help = 'Generate daily summary report for all users'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        users = User.objects.all()
        
        self.stdout.write(self.style.SUCCESS(f'\n=== Daily Summary Report - {today_start.strftime("%Y-%m-%d")} ===\n'))
        
        for user in users:
            visitors = Visitor.objects.filter(
                created_by=user,
                entry_time__gte=today_start
            )
            
            total = visitors.count()
            in_count = visitors.filter(status='IN').count()
            out_count = visitors.filter(status='OUT').count()
            long_staying = visitors.filter(
                status='IN',
                entry_time__lt=now - timedelta(hours=4)
            ).count()
            
            if total > 0:
                self.stdout.write(f'\nUser: {user.username}')
                self.stdout.write(f'  Total Visitors: {total}')
                self.stdout.write(f'  Currently IN: {in_count}')
                self.stdout.write(f'  Checked OUT: {out_count}')
                if long_staying > 0:
                    self.stdout.write(self.style.WARNING(f'  ⚠️  Long Staying (>4hrs): {long_staying}'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Daily summary generated successfully\n'))
