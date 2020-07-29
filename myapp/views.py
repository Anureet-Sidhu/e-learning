# Import necessary classes
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from .models import Topic, Course, Student, Order
from django.shortcuts import get_object_or_404, render
from .forms import OrderForm, InterestForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'top_list': top_list})

def about(request):
    return render(request, 'myapp/about.html')

def detail(request, top_id):
    topic = get_object_or_404(Topic, pk=top_id)
    name = topic.name
    category = topic.category
    course_list = Course.objects.filter(topic__name= str(topic.name))
    return render(request, 'myapp/detail.html', {'course_list': course_list, 'category': category, 'name': name})

def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'courlist': courlist})

def place_order(request):
    msg = ''
    courlist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.levels <= order.course.stages:
                order.save()
                if order.course.price > 150:
                    order.course.discount()
                msg = 'Your course has been ordered successfully.'
            else:
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'courlist': courlist})

def course_detail(request, course_id):
    msg = ''
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'GET':
        form = InterestForm()
        msg = 'Courses'
        return render(request, 'myapp/course_detail.html', {'form': form, 'course': course})
    else:
        if request.method == 'POST':
            form = InterestForm(request.POST)
            if form.is_valid():
                obj = form.cleaned_data['interested']
                if obj == '1':
                    course.interested = course.interested + 1
                    course.save()
                    top_list = Topic.objects.all().order_by('id')[:10]
                    return render(request, 'myapp/index.html', {'top_list': top_list})
                else:
                    msg = 'You are not interested in this course!'
                return render(request, 'myapp/course_detail.html', {'form': form, 'course': course, 'msg': msg})
        else:
            form = InterestForm()
            msg = 'Please select a valid option!'
        return render(request, 'myapp/course_detail.html', {'form': form, 'course': course, 'msg': msg})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        logout(request)
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))

@login_required
def myaccount(request):
    current_user = request.user
    if Student.objects.filter(pk=current_user.id).exists():
        student_obj = Student.objects.get(pk=current_user.id)
        order_obj = Order.objects.filter(student=student_obj)
        interested_obj = Topic.objects.filter(id__in=(Student.objects.values_list('interested_in', flat=True).
                                                      filter(first_name=student_obj.id)))
        return render(request, 'myapp/myaccount.html', {'student_obj': student_obj, 'order_obj': order_obj,
                                                        'interested_obj': interested_obj})
    else:
        return render(request, 'myapp/myaccount.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            msg = 'Student has been registered successfully'
            top_list = Topic.objects.all().order_by('id')[:10]
            return render(request, 'myapp/index.html', {'top_list': top_list, 'msg': msg})
        else:
            msg = 'Student registration failed. Please provide valid data!'
            form = RegisterForm()
            return render(request, 'myapp/register.html', {'msg': msg, 'form': form})
    else:
        form = RegisterForm()
        return render(request, 'myapp/register.html', {'form': form})