from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
import numpy as np
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import UpdateView, DeleteView
from django.core.exceptions import BadRequest
from pathlib import Path
import os
import cv2
from imutils.video import VideoStream
from django.conf import settings

from .forms import EmployeeForm, EmployeeScheduleForm
from .models import Employee, EmployeeSchedule, User
from .tables import EmployeeHTMxTable, EmployeeScheduleHTMxTable
from .filters import EmployeeFilter, EmployeeScheduleFilter

from django_tables2 import SingleTableMixin
from django_filters.views import FilterView

# Path to Haarcascade file
HAAR_CASCADE_PATH = os.path.join(settings.BASE_DIR, "haarcascades", "haarcascade_frontalface_default.xml")

class EmployeeHTMxTableView(SingleTableMixin, FilterView):
    table_class = EmployeeHTMxTable
    queryset = Employee.objects.all()
    filterset_class = EmployeeFilter
    paginate_by = 2

    def get_template_names(self):
        if self.request.htmx:
            template_name = "view_employee_list_htmx_partial.html"
        else:
            template_name = "view_employee_list_htmx.html"

        return template_name

class EmployeeScheduleHTMxTableView(SingleTableMixin, FilterView):
    table_class = EmployeeScheduleHTMxTable
    queryset = EmployeeSchedule.objects.all()
    filterset_class = EmployeeScheduleFilter
    paginate_by = 2

    def get_template_names(self):
        if self.request.htmx:
            template_name = "view_schedule_list_htmx_partial.html"
        else:
            template_name = "view_schedule_list_htmx.html"

        return template_name


class EmployeeEditView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee_edit_form.html'
    success_url = reverse_lazy('view_employee_list')  # Redirect to the employee list page after successful edit

    def get_object(self, queryset=None):
        # Retrieve the employee object by primary key (from the URL)
        return get_object_or_404(Employee, pk=self.kwargs['pk'])

    def form_valid(self, form):
        # Save the form and redirect to the success URL
        self.object = form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form is invalid, render the same form with error messages
        return self.render_to_response(self.get_context_data(form=form))

class EmployeeDeleteView(DeleteView):
    model = Employee
    #template_name = 'employee_confirm_delete.html'  # Optional: Confirmation template
    success_url = reverse_lazy('view_employee_list')  # Redirect after successful deletion

    def get_object(self, queryset=None):
        return get_object_or_404(Employee, pk=self.kwargs['pk'])

class EmployeeScheduleEditView(UpdateView):
    model = EmployeeSchedule
    form_class = EmployeeScheduleForm
    template_name = 'employee_schedule_edit_form.html'
    success_url = reverse_lazy('view_schedule_list')  # Redirect to the employee list page after successful edit

    def get_object(self, queryset=None):
        # Retrieve the employee object by primary key (from the URL)
        return get_object_or_404(EmployeeSchedule, pk=self.kwargs['pk'])

    def form_valid(self, form):
        # Save the form and redirect to the success URL
        self.object = form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form is invalid, render the same form with error messages
        return self.render_to_response(self.get_context_data(form=form))
    
class EmployeeScheduleDeleteView(DeleteView):
    model = EmployeeSchedule
    #template_name = 'employee_schedule_confirm_delete.html'  # Optional: Confirmation template
    success_url = reverse_lazy('view_schedule_list')  # Redirect after successful deletion

    def get_object(self, queryset=None):
        return get_object_or_404(EmployeeSchedule, pk=self.kwargs['pk'])

def camera_view(request):
    return render(request, 'face_access.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def add_employee(request):
    if request.method == 'POST':
        employee_form = EmployeeForm(request.POST)
        if employee_form.is_valid():
            # Save the form and associate the selected user account with the employee
            employee = employee_form.save(commit=False)
            user_id = request.POST.get('user')  # Retrieve the selected user ID
            if user_id:
                employee.linked_account = User.objects.get(id=user_id)
            employee.save()
            return redirect('view_employee_list')  # Redirect to a list or detail view
        else:
            print(employee_form.errors)
    else:
        employee_form = EmployeeForm()

    users = User.objects.exclude(employee__isnull=False)  # Assuming 'employee' is the related name for the User-Employee relationship
    return render(request, 'add_employee.html', {'employee_form': employee_form, 'users': users})

def add_schedule(request):
    if request.method == 'POST':
        schedule_form = EmployeeScheduleForm(request.POST)
        if schedule_form.is_valid():
            # Save the schedule data
            schedule_form.save()
            return redirect('view_schedule_list')  # Redirect to a list or detail view
        else:
            print(schedule_form.errors)
    else:
        schedule_form = EmployeeScheduleForm()

    return render(request, 'add_schedule.html', {'schedule_form': schedule_form})

def open_camera(request):
    return render(request, 'attendance_open_camera.html')

def create_dataset(request):
    if request.method == "POST":
        username = request.POST.get("username")  # Get the username from POST data
        
        # Validate the username
        if not username:
            return JsonResponse({"error": "Username is required."}, status=400)
        
        # Create directory for the user inside the static folder
        directory = os.path.join(settings.BASE_DIR, 'core', 'static', 'registered_faces', username)
        os.makedirs(directory, exist_ok=True)

        # Initialize Haar Cascade for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        # Initialize the webcam
        cap = cv2.VideoCapture(0)
        sampleNum = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            if len(faces) == 0:
                print("No faces detected")
            
            for (x, y, w, h) in faces:
                sampleNum += 1
                face = frame[y:y+h, x:x+w]
                filename = os.path.join(directory, f"{sampleNum}.jpg")
                cv2.imwrite(filename, face)
                print(f"Saving image: {filename}")
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

                if sampleNum >= 10:  # Capture 10 images
                    break

            cv2.imshow("Capturing Images", frame)

            # Break the loop if 'q' is pressed or sample limit is reached
            if cv2.waitKey(1) & 0xFF == ord('q') or sampleNum >= 10:
                break

        cap.release()
        cv2.destroyAllWindows()

        return JsonResponse({"message": "Dataset created successfully!"})

    return render(request, "create_dataset.html")