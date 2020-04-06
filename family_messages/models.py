from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
