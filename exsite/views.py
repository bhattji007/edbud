from django.shortcuts import render, redirect
from django.http import HttpResponse
from exsite.models import Teacher, Question
import random, datetime
from django.core.mail import send_mail
from examsite.settings import EMAIL_HOST_USER

# Create your views here.
def index(request):
    incorrect = False
    if request.session.has_key('user'):
        teachemail = request.session['user']
        userd = Teacher.objects.get(email=teachemail)
        quesppr = Question.objects.filter(pprteach=teachemail).order_by('-id')[:5][::-1]
        # mcqtest = Mcqque.objects.get(pprcode="ComputersDhruv Mishra2020-07-02 12:34:03.001219")
        
        params = {'teacherinfo':userd, 'quesppr':quesppr}
        return render(request,'exsite/teachdashboard.html', params)
    
    elif request.method=='POST':
        teachemail = request.POST.get('email','')
        teachpass = request.POST.get('password','')
        
        if teachemail!='':
            #  to get a particular value from a single query
            try:
                userd = Teacher.objects.get(email=teachemail)
            except Exception:
                incorrect = True
            # to use object data userd.name and so on
        
        
            if (incorrect==False):
                if (teachpass==userd.password):
                    request.session['user'] = teachemail
                    quesppr = Question.objects.filter(pprteach=teachemail).order_by('-id')[:5][::-1]
                    params = {'teacherinfo':userd, 'quesppr':quesppr}
                    return render(request,'exsite/teachdashboard.html', params)
                else:
                    incorrect = True
        
 
    return render(request, 'exsite/index.html',{'incorrect':incorrect})

def teachregister(request):
    if request.method == 'POST':
        name = request.POST.get('Rname','')
        email = request.POST.get('Remail','')
        phone = request.POST.get('Rphone','')
        password = request.POST.get('Rpassword','')
        if Teacher.objects.filter(email = email).exists():
            return render(request, 'exsite/index.html',{'emailexist':True})
            
        else:
            teacher = Teacher(name=name, phone=int(phone), email=email,password=password)
            teacher.save()  
            return redirect('/exsite/otpverify/'+str(email)+'/')
            
    return render(request, 'exsite/index.html',{'incorrect':False})

    
def logout(request):
    try:
        del request.session['user']
    except KeyError:
        pass
    return redirect('/exsite/')

def forgotpass(request):
    if request.method=='POST':
        
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
    
        if Teacher.objects.filter(email=email,phone=phone).exists():
            userd = Teacher.objects.get(email=email,phone=phone)
            
            return redirect('/exsite/otpverify/'+str(email)+'/')
        else:
            return render(request, 'exsite/forgotpassword.html',{'notmatch':True})
        
    return render(request, 'exsite/forgotpassword.html')

def otpverification(request, email):
    user=Teacher.objects.get(email=email)
    if request.method == 'GET':
        otp= random.randint(10000,99999)
        user.otp = otp
        user.save()
        subject = 'Account Verification'
        message = 'This is Your One time password do not share it with anybody\n' + str(otp)
        recepient = str(email)
        send_mail(subject, 
            message, EMAIL_HOST_USER, [recepient], fail_silently = False)
    if request.method == 'POST':
        otpenter = request.POST.get('otpenter','')
        if (otpenter == user.otp):
            request.session['user'] = email
            return redirect('/exsite/')
        else:
            return render(request, 'exsite/otpverify.html',{'wrongotp':True})

    return render(request, 'exsite/otpverify.html')





def norques(request):
    if request.session.has_key('user'):
        teachemail = request.session['user']
        userd = Teacher.objects.get(email=teachemail)
        
        pprname = request.POST.get('pprname','')
        n = request.POST.get('noq','')
        
        if (pprname!='' and n!=''):
        
            return redirect ('/exsite/norques/'+n+'/' + pprname + '/')
            
        params = {'teacherinfo':userd,'quesinfo':True}
        return render(request, 'exsite/norques.html',params)
    return redirect('/exsite/')

def norquesset(request,n,pn):
    if request.session.has_key('user'):
        teachemail = request.session['user']
        userd = Teacher.objects.get(email=teachemail)
        sum=""
        noq=[]
        for i in range(int(n)):
            noq.append(i+1)

        for i in range(int(n)):
            b=request.POST.get('question'+str(i+1),'')
            if (b!=''):
                sum = sum + b +'@#$%'
   
        pdf = request.POST.get('pdf','No')
        stime = request.POST.get('starttime','')
        etime = request.POST.get('endtime','')
        if (sum!=''):
            pprcode = pn + userd.name + str(datetime.datetime.now())
            question = Question(pprname=pn , noofques=int(n), question=sum, pprteach=teachemail,pprcode=pprcode,pdfop=pdf,starttime=stime,endtime=etime)
            question.save()
            ques = Question.objects.get(pprcode=pprcode)
            params = {'teacherinfo':userd,'quesid':True,'ques':ques}
            return render(request, 'exsite/norques.html',params)
        params = {'teacherinfo':userd,'question':True,'noq':noq}
        return render(request, 'exsite/norques.html',params)
    return redirect('/exsite/')

def mcqques(request):
    if request.session.has_key('user'):
        teachemail = request.session['user']
        userd = Teacher.objects.get(email=teachemail)
        
        pprname = request.POST.get('pprname','')
        n = request.POST.get('noq','')
        # print(pprname,n)
        if (pprname!='' and n!=''):
        
            return redirect ('/exsite/mcqques/'+n+'/' + pprname + '/')
            
        params = {'teacherinfo':userd,'quesinfo':True}
        return render(request, 'exsite/mcqques.html',params)
    return redirect('/exsite/')

def mcqquesset(request,n,pn):
    if request.session.has_key('user'):
        teachemail = request.session['user']
        userd = Teacher.objects.get(email=teachemail)
        noq=[]
        for i in range(int(n)):
            noq.append(i+1)
        ques=""
        for i in range(int(n)):
            b=request.POST.get('question'+str(i+1),'')
            op1 = request.POST.get(str(i+1)+'op1','')
            op2 = request.POST.get(str(i+1)+'op2','')
            op3 = request.POST.get(str(i+1)+'op3','')
            op4 = request.POST.get(str(i+1)+'op4','')
            ans = request.POST.get('ans'+str(i+1),'')
            marks = request.POST.get('marks'+str(i+1),'')
            if (b!=''):
                ques = ques + b + '@#$%' + op1 + '@#$%' + op2 + '@#$%' + op3 + '@#$%' + op4 + '@#$%' + ans + '@#$%' + marks + '@#$%'

        stime = request.POST.get('starttime','')
        etime = request.POST.get('endtime','')
        if (stime!=''):
            pprcode = pn + "mcqs" + str(datetime.datetime.now())
            mcq = Question(pprname = pn, noofques = n, question = ques, pprteach = teachemail, pprcode=pprcode, pdfop = "No",starttime=stime,endtime=etime)
            mcq.save()
            ques = Question.objects.get(pprcode=pprcode)
            params = {'teacherinfo':userd,'quesid':True,'ques':ques}
            return render(request, 'exsite/norques.html',params)
        params = {'teacherinfo':userd,'question':True,'noq':noq}
        return render(request, 'exsite/mcqques.html',params)
        
    return redirect('/exsite/')

def teachreview(request,code):
    if request.session.has_key('user'):
        teachemail = request.session['user']
        userd = Question.objects.get(pprcode=code,pprteach=teachemail)
        if request.method == 'POST':
            review = request.POST.get('review','')
            userd.review= review
            userd.save()
            if review!='':
                subject = 'Review from teacher ' + str(teachemail)
                message = 'From ' + str(teachemail) +":-\n"+str(review)
                recepient = 'edbudexaminations@gmail.com'
                send_mail(subject, 
                    message, EMAIL_HOST_USER, [recepient], fail_silently = False)
            return redirect('/exsite/')
    return redirect('/exsite/')