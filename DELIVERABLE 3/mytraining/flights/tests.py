from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from .models import Module, Enrollment

class BasicTests(TestCase):

    def setUp(self):
        # Create test user and module
        self.user = User.objects.create_user(username='testuser', password='pass1234')  # Test user
        self.module = Module.objects.create(
            title='Python Basics',  # Module title
            description='Learn Python.',  # Module description
            start_date='2025-05-01',  # Start date
            trainer=self.user  # Trainer
        )

    def test_module_str(self):
        self.assertEqual(str(self.module), 'Python Basics')  # Check module title

    def test_enrollment_creation(self):
        enrollment = Enrollment.objects.create(student=self.user, module=self.module)  # Create enrollment
        self.assertEqual(enrollment.module.title, 'Python Basics')  # Check module title
        self.assertEqual(enrollment.student.username, 'testuser')  # Check student username

    def test_homepage_access(self):
        response = self.client.get(reverse('home'))  # Access homepage
        self.assertEqual(response.status_code, 200)  # Check if it loads

    def test_enroll_view(self):
        self.client.login(username='testuser', password='pass1234')  # Log in
        response = self.client.get(reverse('enroll', args=[self.module.id]))  # Enroll in module
        self.assertEqual(response.status_code, 302)  # Check redirect
        self.assertTrue(Enrollment.objects.filter(student=self.user, module=self.module).exists())  # Check enrollment

    def test_module_video_requires_enrollment(self):
        self.client.login(username='testuser', password='pass1234')  # Log in
        response = self.client.get(reverse('module_video', args=[self.module.id]))  # Try to watch video
        self.assertRedirects(response, reverse('home'))  # Should redirect if not enrolled

    def test_module_video_allows_enrolled(self):
        Enrollment.objects.create(student=self.user, module=self.module)  # Enroll user
        self.client.login(username='testuser', password='pass1234')  # Log in
        response = self.client.get(reverse('module_video', args=[self.module.id]))  # Watch video
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, 'Python Basics')  # Check content

    def test_register_page_loads(self):
        response = self.client.get(reverse('register'))  # Access register page
        self.assertEqual(response.status_code, 200)  # Check if it loads
        self.assertContains(response, "Register")  

    def test_trainer_dashboard_requires_login(self):
        response = self.client.get(reverse('trainer_dashboard'))  # Access trainer dashboard
        self.assertRedirects(response, '/accounts/login/?next=/trainer/')  # Should redirect if not logged in

    def test_coordinator_dashboard_access(self):
        coordinator_group = Group.objects.create(name='Coordinator')  # Create coordinator group
        self.user.groups.add(coordinator_group)  # Add user to group
        self.client.login(username='testuser', password='pass1234')  # Log in
        response = self.client.get(reverse('coordinator_dashboard'))  # Access coordinator dashboard
        self.assertEqual(response.status_code, 200)  
