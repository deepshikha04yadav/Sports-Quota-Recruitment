from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('admin_login', views.admin_login, name="admin_login"),
    path('captcha/', include('captcha.urls')),
    path('check-captcha/', views.check_captcha, name='check_captcha'),
    path('regenerate-captcha/', views.regenerate_captcha, name='regenerate_captcha'),
    path('applications/', views.applications, name='applications'),
    path('applications/', views.applications_list, name='applications_list'),
    path('applications/<int:app_id>/', views.application_detail, name='application_detail'),
    path('review/<int:app_id>/', views.review_application, name='review_application'),
    path('check_status', views.check_status, name='check_status'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('logout/', views.logout_view, name='logout'),
]

from django.conf import settings
from django.conf.urls.static import static


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
