from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about', views.about, name='about'),
    path(r'<int:top_id>/', views.detail, name='detail'),
    path(r'courses', views.courses, name='courses'),
    path(r'place_order', views.place_order, name='place_order'),
    path(r'courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path(r'login', views.user_login, name='login'),
    path(r'logout', views.user_logout, name='logout'),
    path(r'myaccount', views.myaccount, name='myaccount'),
    path(r'register', views.register, name='register'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)