from django.http import HttpResponse
from django.shortcuts import render, redirect
from exsite.models import Contact
from django.core.mail import send_mail
from examsite.settings import EMAIL_HOST_USER

def home(request):
    return render(request, 'edbudhome.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        name= request.POST.get('contactname','')
        email= request.POST.get('contactemail','')
        message = request.POST.get('contactmsg','')
        contact = Contact(contactname=name, contactemail=email, contactmsg= message)
        contact.save()
        subject = 'Message From ' + str(email)
        message = str(name) + ":\n"+ message
        recepient = 'edbudexaminations@gmail.com'
        send_mail(subject, 
             message, EMAIL_HOST_USER, [recepient], fail_silently = False)
    return render(request, 'contact.html')

def howto(request):
    return render(request, 'howto.html')