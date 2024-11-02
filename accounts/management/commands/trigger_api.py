import time
import requests
from django.core.management.base import BaseCommand
from decouple import config

BACKEND_URL = config("BACKEND_URL")

class Command(BaseCommand):
    help = 'Trigger an API call every 20 seconds'

    def handle(self, *args, **kwargs):
        api_url = f'{BACKEND_URL}/accounts/check/'  # Replace with your API URL

        try:
            while True:
                # Make the API call
                response = requests.get(api_url)
                self.stdout.write(f"API response: {response.status_code}")

                # Sleep for 30 seconds before the next request
                time.sleep(20)
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("Stopped API trigger manually"))
