from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    phone = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Owner(models.Model):
    shop_name = models.CharField(max_length=255)
    account = models.OneToOneField(Account, on_delete=models.CASCADE)


class Employee(models.Model):
    EMPLOYEE_TYPE_CHOICES = [
        ('PURCHASING_OFFICER', 'PURCHASING_OFFICER'),
        ('SALE_OFFICER', 'SALE_OFFICER')
    ]
    department = models.CharField(max_length=18, choices=EMPLOYEE_TYPE_CHOICES, null=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    owner_id = models.ForeignKey(Owner, on_delete=models.CASCADE)
