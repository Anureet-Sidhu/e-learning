import decimal

from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)

    def __str__(self): return str(self.name)

class Course(models.Model):
    topic = models.ForeignKey(Topic, related_name='courses',on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    interested = models.PositiveIntegerField(default=0)
    stages = models.PositiveIntegerField(default=3)

    def __str__(self): return str(self.name)

    def discount(self):
        newPrice = self.price - decimal.Decimal(0.1) * self.price
        return newPrice

class Student(User):
    CITY_CHOICES = [('WS', 'Windsor'),
    ('CG', 'Calgery'), ('MR', 'Montreal'), ('VC', 'Vancouver')]
    school = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic)

    def __str__(self): return str(self.username)

class Order(models.Model):
    course = models.ForeignKey(Course, related_name='courses',on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='students', on_delete=models.CASCADE,  default=None)
    ORDER_CHOICES = [(0, 'Cancelled'),
                    (1, 'Order Confirmed')]
    order_status = models.IntegerField(choices= ORDER_CHOICES, default=1)
    levels = models.PositiveIntegerField(default=1)
    order_date = models.DateField()

    def __str__(self): return str(self.course.name + ' by ' + self.student.first_name + self.student.last_name)

    def total_cost(self):
        totalCost = 0
        for course in self.course:
            totalCost = course.price + totalCost
        return totalCost
