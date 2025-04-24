from django.db import models
from django.contrib.auth.models import User

# Module model
class Module(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="modules")
    video_url = models.URLField(blank=True, null=True)  # field for video

    def __str__(self):
        return self.title

# Enrollment model
class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_on = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'module')
