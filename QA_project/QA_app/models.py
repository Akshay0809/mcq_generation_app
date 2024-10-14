from django.db import models

# Create your models here.

class MCQ(models.Model):
    question=models.TextField()
    created_at=models.DateField(auto_now_add=True)
    is_current = models.BooleanField(default=True)  # Flag to indicate if it's current


    def __str__(self):
        return self.question
    