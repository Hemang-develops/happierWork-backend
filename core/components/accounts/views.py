import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

# Path to your JSON file

# Get the current directory of the views.py file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the data.json file
ACCOUNTS_FILE = os.path.join(BASE_DIR, 'accounts.json')
# ACCOUNTS_FILE = 'accounts.json'

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            email = data.get('email')
            password = data.get('password')  # Validate password if needed

            if not email:
                return JsonResponse({'error': 'Email is required'}, status=400)

            email_parts = email.split('@')[0].split('.')
            if len(email_parts) == 2:
                first_name, last_name = email_parts

                user_data = {
                    'first_name': first_name,
                    'last_name': last_name
                }
            else:
                first_name = email_parts
                user_data = {
                    'first_name': first_name,
                    'last_name': ''
                }

            if os.path.exists(ACCOUNTS_FILE):
                with open(ACCOUNTS_FILE, 'r') as file:
                    accounts = json.load(file)
            else:
                accounts = []

            accounts.append(user_data)

            with open(ACCOUNTS_FILE, 'w') as file:
                json.dump(accounts, file, indent=4)

            return JsonResponse({'message': 'Login successful'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)