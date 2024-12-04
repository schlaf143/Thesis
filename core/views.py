from django.shortcuts import render
from django.http import JsonResponse
import base64
from io import BytesIO
from PIL import Image
import numpy as np

def camera_view(request):
    return render(request, 'face_access.html')

def upload_photo(request):
    if request.method == 'POST':
        try:
            # Get the photo data from the request body
            photo_data = request.POST.get('photo')

            # Decode the base64 string
            photo_data = photo_data.split(',')[1]
            img_data = base64.b64decode(photo_data)
            image = Image.open(BytesIO(img_data))

            # Here you can add any image processing or recognition logic
            # For now, we'll just return success
            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})
