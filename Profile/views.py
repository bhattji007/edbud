from django.shortcuts import render, redirect
from django.http import HttpResponse
from exsite.models import Teacher, Question, Student
import math,os

# Create your views here.
def profile(request):
    if request.session.has_key('user'):
        teachemail = request.session['user']
        userp = Teacher.objects.get(email=teachemail)
        return render(request, 'Profile/userprofile.html', {'teacherinfo':userp})
    return redirect('/exsite/')

def changepro(request):
    if request.session.has_key('user'):
        teachemail = request.session['user']
        userp = Teacher.objects.get(email=teachemail)
        nomatch = False
        if request.method == 'POST':
            chngname = request.POST.get('chngname','')
            chngphone = request.POST.get('chngphone','')
            description = request.POST.get('description','')
            userp.name= chngname
            userp.phone = chngphone
            userp.description = description
            userp.save()
            oldpass = request.POST.get('oldpass','')
            chngpass = request.POST.get('chngpass','')
            nomatch = False
            if (oldpass!=''):
                if(oldpass == userp.password):
                    userp.password = chngpass
                    userp.save()
                else:
                    nomatch = True
                    return render(request, 'Profile/changeprofile.html', {'teacherinfo':userp, 'nomatch':nomatch})
            return redirect('/userprofile/')
        return render(request, 'Profile/changeprofile.html', {'teacherinfo':userp, 'nomatch':nomatch})

    return redirect('/exsite/')


def allquestion(request):
    if request.session.has_key('user'):
        teachemail = request.session['user']
        userd = Teacher.objects.get(email=teachemail)
        quesset = Question.objects.filter(pprteach=teachemail).order_by('-id')
        last = math.ceil(len(quesset)/int(2))
        page = (request.GET.get('page'))
        if(not str(page).isnumeric()):
            page = 1
        page = int(page) 
        ques = quesset[(page-1)*int(2):(page-1)*int(2)+int(2)]
        '''previous and newer buttons handling
        1. user on first page'''
        if(page==1):
            one=True
            prev = "#"
            next = "/userprofile/allquestion?page=" + str(page + 1)
        # 3. user in last page
        elif(page==last):
            last=True
            prev = "/userprofile/allquestion?page=" + str(page - 1)
            next = "#"
        # 2. user in middle page
        else:
            prev = "/userprofile/allquestion?page=" + str(page - 1)
            next = "/userprofile/allquestion?page=" + str(page + 1)
        
            
        return render(request, 'Profile/allquestion.html', {'teacherinfo':userd,'quesset':ques,'next':next,'prev':prev})
    return redirect('/exsite/')

def questionview(request,code):
    if request.session.has_key('user'):
        teachemail = request.session['user']
        userp = Teacher.objects.get(email=teachemail)
        submissions = Student.objects.filter(pprcode=code)
        test = Question.objects.get(pprcode=code)
        if "mcqs" in code:
            # mcq= True
            return render(request, 'Profile/submissions.html',{'teacherinfo':userp,'submissions':submissions,'code':code,'mcq':True})
        elif test.pdfop=="Yes":
            # pdf=True
            return render(request, 'Profile/submissions.html',{'teacherinfo':userp,'submissions':submissions,'code':code,'pdfs':True})
        else:
            # normal=True
            return render(request, 'Profile/submissions.html',{'teacherinfo':userp,'submissions':submissions,'code':code,'normal':True})

    return redirect('/exsite/')

def norquesview(request, code, email):
    if request.session.has_key('user'):
        teachemail = request.session['user']
        userp = Teacher.objects.get(email=teachemail)
        questset = Question.objects.get(pprcode=code)
        student = Student.objects.get(studemail=email, pprcode=code)
        data1=[n for n in range(len(questset.question)) if questset.question.find("@#$%", n) == n]
        j=0
        ques=[]
        for i in range (len(data1)):
            ques.append(questset.question[j:data1[i]])
            j=data1[i]+4

        data2=[n for n in range(len(student.result)) if student.result.find("@#$%", n) == n]
        j=0
        ans=[]
        for i in range (len(data2)):
            ans.append(student.result[j:data2[i]])
            j=data2[i]+4

        mylist = zip(ques,ans)
        return render(request, 'Profile/viewnoranswers.html',{'teacherinfo':userp,'mylist':mylist,'studentinfo':student})
    return redirect('/exsite/')

def quesviewer(request, code):
    if request.session.has_key('user'):
        teachemail = request.session['user']
        userp = Teacher.objects.get(email=teachemail)
        questset = Question.objects.get(pprcode=code)
        if "mcqs" in code:
            if request.method =='POST':
                ques=""
                for i in range(int(questset.noofques)):
                    b=request.POST.get('question'+str(i+1),'')
                    op1 = request.POST.get(str(i+1)+'op1','')
                    op2 = request.POST.get(str(i+1)+'op2','')
                    op3 = request.POST.get(str(i+1)+'op3','')
                    op4 = request.POST.get(str(i+1)+'op4','')
                    ans = request.POST.get('ans'+str(i+1),'')
                    marks = request.POST.get('marks'+str(i+1),'')
                    
                    if (b!=''):
                        ques = ques + b + '@#$%' + op1 + '@#$%' + op2 + '@#$%' + op3 + '@#$%' + op4 + '@#$%' + ans + '@#$%' + marks + '@#$%'
                questset.question=ques
                questset.save()
            data1=[n for n in range(len(questset.question)) if questset.question.find("@#$%", n) == n]
            j=0
            ques=[]
            for i in range (len(data1)):
                ques.append(questset.question[j:data1[i]])
                j=data1[i]+4
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
            return render(request, 'Profile/quesviewer.html',{'teacherinfo':userp,'questions':final, 'pprinfo':questset,'mcq':True})
        else:
            if request.method == 'POST':
                sum=""
                for i in range(int(questset.noofques)):
                    b=request.POST.get('question'+str(i+1),'')
                    if (b!=''):
                        sum = sum + b +'@#$%'
                questset.question=sum
                questset.save()
            data1=[n for n in range(len(questset.question)) if questset.question.find("@#$%", n) == n]
            j=0
            ques=[]
            for i in range (len(data1)):
                ques.append(questset.question[j:data1[i]])
                j=data1[i]+4
                a=[]
            
            return render(request, 'Profile/quesviewer.html',{'teacherinfo':userp,'questions':ques, 'pprinfo':questset})
        
    return redirect('/exsite/')

def deleteppr(request, code):
    if request.session.has_key('user'):
        if request.method=='POST':
            ques = Question.objects.get(pprcode=code)
            ans = Student.objects.filter(pprcode=code)
            ques.delete()
            for submission in ans:
                submission.delete()
            return redirect('/userprofile/allquestion/')
    return redirect('/exsite/')
