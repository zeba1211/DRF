from django.db import models

# Create your models here.
from django.db import models
from api.models import Employee  # Assuming the Employee model is in the 'employee' app
from api.models import Company  # Assuming the Company model is in the 'company' app

class Department(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    head = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    deadline = models.DateField()
    status = models.CharField(max_length=50, choices=[('Ongoing', 'Ongoing'), ('Completed', 'Completed'), ('On Hold', 'On Hold')])
    budget_allocated = models.DecimalField(max_digits=10, decimal_places=2)
    manager = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
