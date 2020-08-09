from django.contrib import admin
from django.db import models

from .forms import OrderForm
from .models import Topic, Course, Student, Order
from django.contrib import admin


def upper_case_name(obj):
    return ("%s %s" % (obj.first_name, obj.last_name)).upper()


upper_case_name.short_description = 'Student Full Name'


class StudentAdmin(admin.ModelAdmin):
    list_display = (upper_case_name, 'city')
    list_filter = ('city', 'school')
    search_fields = ('name__startswith',)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'price', 'hours', 'for_everyone')
    list_filter = ('for_everyone', 'topic', 'price')
    search_fields = ('name__startswith',)
    actions = ['add_50_to_hours']

    def add_50_to_hours(self, request, queryset):
        for hour in queryset.all():
            queryset.update(hours=(int(hour.hours) + 10))

    add_50_to_hours.short_description = 'Add 10 Hours'


class TopicAdmin(admin.ModelAdmin):
    list_filter = ('category', 'name')
    list_display = ('name', 'category')
    search_fields = ('name__startswith',)


def upper_case_student_name(obj):
    return ("%s" % obj.student.first_name).capitalize()


upper_case_student_name.short_description = 'Order By'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('course', upper_case_student_name, 'order_status', 'levels')
    list_filter = ('order_status', 'levels', 'order_date')
    search_fields = ('student__first_name__startswith',)
    actions = ['cancel_order', 'confirm_order', 'add_level']

    def cancel_order(self, request, queryset):
        queryset.update(order_status=0)

    def confirm_order(self, request, queryset):
        queryset.update(order_status=1)

    def add_level(self, request, queryset):
        for order in queryset.all():
            queryset.update(levels=(int(order.levels) + 1))

    cancel_order.short_description = 'Cancel Order'
    confirm_order.short_description = 'Confirm Order'
    add_level.short_description = "Add level by 1"


# Register your models here.
admin.site.register(Topic, TopicAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Order, OrderAdmin)
