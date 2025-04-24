from django.shortcuts import render, redirect
from .models import Module, Enrollment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.db.models import Q  # For search support

# Check if user is a coordinator (Group-based)
def is_coordinator(user):
    return user.groups.filter(name='Coordinator').exists()

# Role-based login redirect
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return '/admin/'
        elif user.is_staff:
            return '/trainer/'
        elif is_coordinator(user):
            return '/coordinator/'
        else:
            return '/'

# Home view with search
def home(request):
    query = request.GET.get('q', '')
    if query:
        modules = Module.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    else:
        modules = Module.objects.all()

    enrolled_ids = []
    if request.user.is_authenticated:
        enrolled_ids = Enrollment.objects.filter(student=request.user).values_list('module_id', flat=True)

    return render(request, 'flights/home.html', {
        'modules': modules,
        'enrolled_ids': enrolled_ids,
        'query': query
    })

# Enroll in module
@login_required
def enroll(request, module_id):
    module = Module.objects.get(id=module_id)
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, module=module)
    if created:
        messages.success(request, f"You are now enrolled in {module.title}.")
    else:
        messages.warning(request, f"You are already enrolled in {module.title}.")
    return redirect('home')

# Register view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Trainer dashboard
@login_required
def trainer_dashboard(request):
    if not request.user.is_staff:  # Check if user is not a trainer
        return redirect('home')  # Send them home
    modules = Module.objects.filter(trainer=request.user)  # Get trainer's modules
    return render(request, 'flights/trainer_dashboard.html', {'modules': modules})  # Show trainer dashboard

# Coordinator dashboard
@login_required
def coordinator_dashboard(request):
    if not is_coordinator(request.user):  # Check if user is not a coordinator
        return redirect('home')  # Send them home

    total_modules = Module.objects.count()  # Count all modules
    total_students = User.objects.filter(is_staff=False).count()  # Count all students
    total_enrollments = Enrollment.objects.count()  # Count all enrollments
    modules = Module.objects.all()  # Get all modules

    return render(request, 'flights/coordinator_dashboard.html', {
        'total_modules': total_modules,  # Pass total modules
        'total_students': total_students,  # Pass total students
        'total_enrollments': total_enrollments,  # Pass total enrollments
        'modules': modules  # Pass all modules
    })

# Module video view
@login_required
def module_video(request, module_id):
    module = Module.objects.get(id=module_id)  # Get the module

    is_enrolled = Enrollment.objects.filter(student=request.user, module=module).exists()  # Check if enrolled
    if not is_enrolled:  # If not enrolled
        messages.warning(request, "You must be enrolled to view this training module.")  # Show warning
        return redirect('home')  # Send them home

    return render(request, 'flights/module_video.html', {'module': module})  # Show module video
