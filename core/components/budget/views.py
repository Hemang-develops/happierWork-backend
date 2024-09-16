import os
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

# Get the current directory of the views.py file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the data.json file
DATA_FILE = os.path.join(BASE_DIR, 'data.json')

@require_http_methods(['GET'])
def read_data(request):
    with open(DATA_FILE, 'r') as file:
        data = json.load(file)
    return JsonResponse(data, safe=False)

@csrf_exempt
@require_http_methods(['POST'])
def create_data(request):
    new_entry = json.loads(request.body)
    
    with open(DATA_FILE, 'r+') as file:
        data = json.load(file)
        data.append(new_entry)  # Add the new entry
        file.seek(0)            # Move the cursor to the beginning of the file
        json.dump(data, file, indent=4)  # Write updated data back
    
    return JsonResponse({'message': 'Data added successfully'}, status=201)

@csrf_exempt
@require_http_methods(['PUT'])
def update_data(request, entry_id):
    updated_entry = json.loads(request.body)

    with open(DATA_FILE, 'r+') as file:
        data = json.load(file)
        for entry in data:
            if entry['id'] == entry_id:
                entry.update(updated_entry)  # Update the entry
                break
        else:
            return JsonResponse({'error': 'Entry not found'}, status=404)

        file.seek(0)
        json.dump(data, file, indent=4)
    
    return JsonResponse({'message': 'Data updated successfully'}, status=200)

@csrf_exempt
@require_http_methods(['DELETE'])
def delete_data(request, entry_id):
    with open(DATA_FILE, 'r+') as file:
        data = json.load(file)
        data = [entry for entry in data if entry['id'] != entry_id]  # Remove the entry
        
        file.seek(0)
        file.truncate()  # Clear the file before writing
        json.dump(data, file, indent=4)
    
    return JsonResponse({'message': 'Data deleted successfully'}, status=204)
