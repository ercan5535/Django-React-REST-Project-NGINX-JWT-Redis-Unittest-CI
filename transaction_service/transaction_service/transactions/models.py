from django.db import models

# Create your models here.
class Transaction(models.Model):
    department = models.CharField(max_length=100)
    amount = models.FloatField()
    created_by = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.department} {self.amount}"