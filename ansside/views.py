from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from exsite.models import Question, Student
import time
from django.core.mail import send_mail
from examsite.settings import EMAIL_HOST_USER
# Create your views here.
def index(request):
    if request.method=='POST':
        prcd = request.POST.get('pprcode')
        name=request.POST.get('studname','')
        email = request.POST.get('studemail','')
        institution = request.POST.get('studinst','')
        rollno = request.POST.get('studrn','')
        paper = get_object_or_404(Question, pprcode=prcd)
        #if the schedule date and time is yet to come
        if (paper.starttime>timezone.now()):
            return render(request, 'ansside/scheduleinfo.html',{'paper':paper,'start':True,'date':paper.starttime})
        # Scheduled date and time started
        else:
            # Scheduled end date and time of examination is yet to come
            if(timezone.now()<=paper.endtime):
                t=paper.endtime-paper.starttime
                hr = t.days*24
                time=(t.seconds/60)
                studinfo = Student(studname=name,studemail=email,studinst=institution,studrn=rollno,pprcode=prcd)
                studinfo.save()
                if 'mcqs' in paper.pprcode:
                    return render(request,'ansside/pprinfo.html',{'paper':paper,'mcq':True,'email':email,'hr':hr,'time':time,'date':paper.starttime.date()})
                else:
                    return render(request,'ansside/pprinfo.html',{'paper':paper,'mcq':False,'email':email,'hr':hr,'time':time,'date':paper.starttime.date()})
            # Scheduled end date and time is over
            else:
                return render(request, 'ansside/scheduleinfo.html',{'paper':paper,'start':False,'date':paper.starttime})
    return render(request, 'ansside/codeEntry.html')


def mcqpapercenter(request,code,email):
    questset = Question.objects.get(pprcode=code)
    
    #if the schedule date and time is yet to come
    if (questset.starttime>timezone.now()):
        return render(request, 'ansside/scheduleinfo.html',{'paper':questset,'start':True,'date':questset.starttime})
    # Scheduled date and time started
    else:
        # Scheduled end date and time of examination is yet to come
        if(timezone.now()<=questset.endtime):
            studinfo = get_object_or_404(Student,studemail=email,pprcode=code)
            #if Student is giving exam first time
            if(studinfo.result==''):
                data=[n for n in range(len(questset.question)) if questset.question.find("@#$%", n) == n]
                j=0
                ques=[]
                for i in range (len(data)):
                    ques.append(questset.question[j:data[i]])
                    j=data[i]+4
                a=[]
                final=[]
                for i in range(len(ques)):
                    if(i==0):
                        a.append(ques[0])
                    elif(i%7==0):
                        final.append(a)
                        a=[]
                        a.append(ques[i])
                    else:
                        a.append(ques[i])
                    if (i==(len(ques)-1)):
                        final.append(a)
                t=questset.endtime-timezone.now()
                timer=t.seconds
                if request.method == 'POST':
                    ans=[]
                    points=[]
                    for set in final:
                        ans.append(set[5])
                        points.append(int(set[6]))
                    marks=0
                    total=0
                    for i in range(1,(len(final)+1)):
                        checking = request.POST.get('mcq'+str(i),False)
                        if(checking==ans[i-1]):
                            marks = marks+points[i-1]
                        total=total+points[i-1]
                            
                    studinfo.subtime=time.asctime(time.localtime(time.time()))
                    studinfo.result = str(marks) + ' out of ' + str(total)
                    studinfo.save()
                    
                    
                    return render(request, 'ansside/resultsub.html', {'studinfo':studinfo,'mcq':True})
                    
                return render(request, 'ansside/mcqexampage.html',{"quesset":final,'time':timer})
            else:
                return render(request, 'ansside/resultsub.html', {'studinfo':studinfo,'mcq':True})
        # Scheduled end date and time is over
        else:
            return render(request, 'ansside/scheduleinfo.html',{'paper':questset,'start':False,'date':questset.starttime})



def normalpapercenter(request,code,email):
    questset = get_object_or_404(Question,pprcode=code)

    #if the schedule date and time is yet to come
    if (questset.starttime>timezone.now()):
        return render(request, 'ansside/scheduleinfo.html',{'paper':questset,'start':True,'date':questset.starttime})
    # Scheduled date and time started
    else:
        # Scheduled end date and time of examination is yet to come
        if(timezone.now()<=questset.endtime):
            studinfo = get_object_or_404(Student,studemail=email,pprcode=code)
            #if Student is giving exam first time
            if(studinfo.result==''):
                if (questset.pdfop =="Yes"):
                    data=[n for n in range(len(questset.question)) if questset.question.find("@#$%", n) == n]
                    j=0
                    ques=[]
                    for i in range (len(data)):
                        ques.append(questset.question[j:data[i]])
                        j=data[i]+4
                    
                    t=questset.endtime-timezone.now()
                    timer=t.seconds
                    return render(request, 'ansside/norexampage.html',{'ques':ques,'pdf':True,'studinfo':studinfo,'time':timer})
                else:
                    data=[n for n in range(len(questset.question)) if questset.question.find("@#$%", n) == n]
                    j=0
                    ques=[]
                    for i in range (len(data)):
                        ques.append(questset.question[j:data[i]])
                        j=data[i]+4
                    t=questset.endtime-timezone.now()
                    timer=t.seconds
                    anslist=""
                    if request.method == 'POST':
                        for i in range(1,(len(ques)+1)):
                            ans = request.POST.get('ans'+str(i),'')
                            if ans=='':
                                ans='No answer given'
                            anslist = anslist + ans + "@#$%"
                        studinfo.subtime=time.asctime(time.localtime(time.time()))
                        studinfo.result = anslist
                        studinfo.save()
                        return render(request, 'ansside/resultsub.html', {'studinfo':studinfo,'mcq':False})
                    return render(request, 'ansside/norexampage.html',{'ques':ques,'pdf':False,'time':timer})
            else:
                return render(request, 'ansside/resultsub.html', {'studinfo':studinfo,'mcq':False})
        # Scheduled end date and time is over
        else:
            return render(request, 'ansside/scheduleinfo.html',{'paper':questset,'start':False,'date':questset.starttime})

def anspdf(request, code, email):
    pdfsumission = get_object_or_404(Student,studemail=email,pprcode=code)
    pdfsumission.result="Pdfsubmitted"
    pdfsumission.save()
    if  request.FILES:
        f= request.FILES.get('anspdf','')
        pdfsumission.pdf=f
        pdfsumission.subtime=time.asctime(time.localtime(time.time()))
        pdfsumission.save()
        return render(request, 'ansside/resultsub.html', {'studinfo':pdfsumission,'mcq':False})
    return render(request, 'ansside/pdfsubmit.html', {'student':pdfsumission})

def review(request, code, email):
    studinfo = get_object_or_404(Student,studemail=email,pprcode=code)
    if request.method =='POST':
        review = request.POST.get('review','')
        studinfo.review=review
        studinfo.save()
        if review!='':
            subject = 'Review from Student ' + str(studinfo.studemail)
            message = 'From ' + str(studinfo.studemail) +":-\n"+str(review)
            recepient = 'edbudexaminations@gmail.com'
            send_mail(subject, 
                message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        
    return redirect('/')
    