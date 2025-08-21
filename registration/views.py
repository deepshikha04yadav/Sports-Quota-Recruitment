import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, User
from .models import Candidate, Document, Application, PhoneOTP, generate_otp
from .forms import CandidateRegistrationForm
from django.utils import timezone
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail



def generate_captcha_text(length=6):
    chars = string.ascii_uppercase + string.digits
    captcha_text = ''.join(random.choices(chars, k=length))
    return captcha_text



def regenerate_captcha(request):
    captcha_code = generate_captcha_text()
    request.session['captcha_code'] = captcha_code
    return JsonResponse({'captcha_code': captcha_code})


def home(request):
    captcha_code = generate_captcha_text()
    request.session['captcha_code'] = captcha_code  # Save to session
    return render(request, "registration/index.html", {'captcha_code': captcha_code})



def check_captcha(request):
    if request.method == 'POST':
        entered = request.POST.get('entered_captcha')
        actual = request.session.get('captcha_code')

        if entered and entered.upper() == actual:
            return render(request, 'success')  # Captcha correct
        else:
            return HttpResponse("Message: Invalid Captcha")
    return redirect('index')



def register(request):
    if request.method == 'POST':
        phone_verified = request.POST.get('phone_verified') == 'true'
        phone_number = request.POST.get('number')
        
        if not phone_verified:
            return render(request, 'register.html', {
                'error': 'Please verify your phone number before submitting.'
            })
        
        # Verify that the phone number was actually verified
        try:
            phone_otp = PhoneOTP.objects.get(phone_number=phone_number)
            if not phone_otp.is_verified:
                return render(request, 'register.html', {
                    'error': 'Phone number not verified.'
                })
        except PhoneOTP.DoesNotExist:
            return render(request, 'register.html', {
                'error': 'Phone verification record not found.'
            })


def register(request):
    if request.method == 'POST':
        # Generate registration number
        last_id = Candidate.objects.count() + 1
        reg_no = f"SPQ{timezone.now().year}{last_id}"

        # Save candidate
        candidate = Candidate.objects.create(
            registration_no=reg_no,
            first_name=request.POST.get('fname'),
            last_name=request.POST.get('lname'),
            email=request.POST.get('email'),
            phone=request.POST.get('number'),
            age=request.POST.get('age'),
            gender=request.POST.get('gender'),
            dob=request.POST.get('dob'),
            photo=request.FILES.get('photo'),
            transaction_no=request.POST.get('transation_no'),
        )

        Application.objects.create(candidate=candidate)

        # Save documents (multiple)
        for doc in request.FILES.getlist('document'):
            Document.objects.create(candidate=candidate, document_file=doc)

        # Pass registration number to success template
        return render(request, 'registration/success.html', {'reg_no': candidate.registration_no})

    return render(request, 'registration/register.html')




def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')  # Make sure this matches the form's "name" attribute

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            # Redirect to admin dashboard, applications list, etc.
            return redirect('applications')
        else:
            # return render(request, 'registration/admin_login.html', {'error': 'Invalid credentials or not superuser.'})
            return HttpResponse("Invalid credentials or not superuser.")
    return render(request, 'registration/admin_login.html')



def applications(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    applications = Application.objects.select_related('candidate').all()
    return render(request, 'registration/applications.html', {'applications': applications})

def applications_list(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    search_reg_no = request.GET.get('search_reg_no', '').strip()
    applications = Application.objects.select_related('candidate').all()
    if search_reg_no:
        applications = applications.filter(candidate__registration_no__icontains=search_reg_no)
    return render(request, "applications.html", {"applications": applications,
    })



def applications_list(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    applications = Application.objects.select_related('candidate').all()
    return render(request, 'registration/applications.html', {'applications': applications})



def application_detail(request, app_id):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    application = get_object_or_404(Application.objects.select_related('candidate'), id=app_id)
    documents = application.candidate.documents.all()  # `related_name='documents'` in Document model
    return render(request, 'registration/application_detail.html', {
        'application': application,
        'documents': documents
    })

def check_status(request):
    status_message = None
    
    if request.method == 'POST':
        reg_no = request.POST.get('registration_no')  # from input name
        entered_captcha = request.POST.get('entered_captcha')
        actual_captcha = request.session.get('captcha_code', '')

        # 1. Validate captcha
        if entered_captcha != actual_captcha:
            status_message = "Invalid captcha!"
        else:
            # 2. Find application by candidate's registration number
            try:
                application = Application.objects.select_related('candidate').get(candidate__registration_no=reg_no)
                status_message = f"Your application status: {application.status}"
            except Application.DoesNotExist:
                status_message = "No application found for this registration number."

    # Always regenerate captcha for next request
    from .views import generate_captcha_text  # or put helper above
    captcha_code = generate_captcha_text()
    request.session['captcha_code'] = captcha_code

    return render(request, 'registration/index.html', {
        'captcha_code': captcha_code,
        'status_message': status_message
    })


def review_application(request, app_id):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    app = get_object_or_404(Application, id=app_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action in ['Accepted', 'Rejected']:
            app.status = action
            app.reviewed_at = timezone.now()
            app.save()

            # Send notification email
            subject = f"Your Sports Quota Application Status: {app.status}"
            message = (
                f"Dear {app.candidate.first_name},\n\n"
                f"Your application ({app.candidate.registration_no}) has been {app.status}."
                "\n\nThank you for applying!\n\n"
                "Regards,\nSports Quota Committee"
            )
            recipient_list = [app.candidate.email]
            send_mail(subject, message, None, recipient_list, fail_silently=False)

    return redirect('applications_list')



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import json

# For sending SMS (you can integrate with Twilio, MSG91, etc.)
def send_otp_sms(phone_number, otp):
    # For development, print to console
    print(f"Sending OTP {otp} to {phone_number}")
    # In production, integrate with SMS gateway:
    # Example with Twilio:
    # from twilio.rest import Client
    # client = Client('your_account_sid', 'your_auth_token')
    # client.messages.create(
    #     body=f'Your OTP is: {otp}',
    #     from_='+1234567890',  # Your Twilio number
    #     to=phone_number
    # )

@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone_number = data.get('phone_number')
        
        if not phone_number:
            return JsonResponse({'success': False, 'message': 'Phone number required'})
        
        # Generate OTP
        otp_code = generate_otp()
        
        # Save or update OTP record
        phone_otp, created = PhoneOTP.objects.update_or_create(
            phone_number=phone_number,
            defaults={'otp': otp_code, 'is_verified': False}
        )
        
        # Send OTP via SMS
        try:
            send_otp_sms(phone_number, otp_code)
            return JsonResponse({'success': True, 'message': 'OTP sent successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Failed to send OTP'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone_number = data.get('phone_number')
        entered_otp = data.get('otp')
        
        try:
            phone_otp = PhoneOTP.objects.get(phone_number=phone_number)
            
            if phone_otp.is_expired:
                return JsonResponse({'success': False, 'message': 'OTP expired'})
            
            if phone_otp.otp == entered_otp:
                phone_otp.is_verified = True
                phone_otp.save()
                return JsonResponse({'success': True, 'message': 'Phone number verified successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid OTP'})
                
        except PhoneOTP.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'OTP not found'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('admin_login')
    return redirect('registration/applications_list')
