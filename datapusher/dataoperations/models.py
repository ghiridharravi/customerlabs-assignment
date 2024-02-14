from django.db import models

class Account(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    account_id = models.CharField(max_length=255, unique=True)
    account_name = models.CharField(max_length=255)
    app_secret_token = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.account_name

class Destination(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='destinations')
    url = models.URLField()
    http_method = models.CharField(max_length=5)
    headers = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return f"{self.account.account_name} - {self.url}"