from django.db import models

class SecurityAuditLog(models.Model):
    event_type = models.CharField(max_length=100)  
    user_ip = models.GenericIPAddressField()
    severity = models.CharField(max_length=20)    
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} - {self.severity} at {self.timestamp}"