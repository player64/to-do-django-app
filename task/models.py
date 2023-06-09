from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Task(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'To-Do'),
        ('DOING', 'Doing'),
        ('DONE', 'Done'),
    ]

    owned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default='TODO')

    class Meta:
        ordering = ["status", "-created_date"]

    def __str__(self):
        return self.title
