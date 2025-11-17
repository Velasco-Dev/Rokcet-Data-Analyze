from django.db import models
import os

class DataFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='csv_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    def filename(self):
        return os.path.basename(self.file.name)