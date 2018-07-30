from django.core.management import BaseCommand, call_command
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Fix the passwords of fixtures"

    def handle(self, *args, **options):
        call_command('loaddata','user_initial_data.json')        
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()