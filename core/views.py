from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import BadRequest
from pathlib import Path
import os

from .forms import EmployeeForm
from .models import Employee
from .tables import EmployeeHTMxTable
from .filters import EmployeeFilter

from django_tables2 import SingleTableMixin
from django_filters.views import FilterView

BASE_DIR = Path(__file__).resolve().parent.parent
EMBEDDINGS_FILE = BASE_DIR / 'face_embeddings.json'

class EmployeeHTMxTableView(SingleTableMixin, FilterView):
    table_class = EmployeeHTMxTable
    queryset = Employee.objects.all()
    filterset_class = EmployeeFilter
    paginate_by = 3

    def get_template_names(self):
        if self.request.htmx:
            template_name = "view_employee_list_htmx_partial.html"
        else:
            template_name = "view_employee_list_htmx.html"

        return template_name

def camera_view(request):
    return render(request, 'face_access.html')

def save_face(request):
    print(f"Embedding File: {EMBEDDINGS_FILE}")
    return render(request, 'face_get.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')  # Redirect to a list or detail view
    else:
        form = EmployeeForm()
    return render(request, 'add_employee.html', {'form': form})


############
def get_embeddings():
    print("Get Embedding function gets called properly")
    if EMBEDDINGS_FILE.exists():
        with open(EMBEDDINGS_FILE, 'r') as file:
            #print(f"File as: {file}")
            return json.load(file)
    return []

def cosine_distance(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    magnitude1 = np.linalg.norm(vec1)
    magnitude2 = np.linalg.norm(vec2)
    return 1 - (dot_product / (magnitude1 * magnitude2))


last_saved_embedding = None
embeddings_buffer = []
MAX_EMBEDDINGS = 5
THRESHOLD = 0.1

@csrf_exempt
def save_face_embedding(request):
    global last_saved_embedding, embeddings_buffer

    if request.method == 'POST':
        try:
            # Extract data from the request
            data = json.loads(request.body.decode('utf-8'))
            name = data.get('name')
            embedding = data.get('embedding')

            if not name or not embedding or not isinstance(embedding, list):
                raise BadRequest("Invalid data format.")

            # Track if the current embedding is too similar to the last one
            if last_saved_embedding is not None:
                distance = cosine_distance(last_saved_embedding, embedding)
                if distance < THRESHOLD:
                    return JsonResponse({'status': 'skipped'}, status=200)  # Skip saving if similar

            # Add current embedding to the buffer
            embeddings_buffer.append(list(embedding))  # Store embedding as list

            # Check if we need to save the buffer
            if len(embeddings_buffer) >= MAX_EMBEDDINGS:
                # Calculate the mean embedding
                mean_embedding = np.mean(embeddings_buffer, axis=0).tolist()

                # Save the mean embedding
                embeddings = get_embeddings()
                embeddings.append({'name': name, 'embedding': mean_embedding})

                # Write the updated embeddings to the file
                with open(EMBEDDINGS_FILE, 'w') as file:
                    json.dump(embeddings, file, indent=4)

                # Clear the buffer after saving
                embeddings_buffer = []
                last_saved_embedding = mean_embedding  # Update last saved embedding

                return JsonResponse({'status': 'success'}, status=200)
            else:
                return JsonResponse({'status': 'buffering'}, status=200)  # Inform that buffering is ongoing

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except BadRequest as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            # Log more details in case of error
            print(f"Error: {str(e)}")
            return JsonResponse({'error': 'An error occurred while processing the request.'}, status=400)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

@csrf_exempt
def get_saved_face_embeddings(request):
    if request.method == 'GET':
        return JsonResponse(get_embeddings(), safe=False)
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


