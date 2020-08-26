from django.db import models
from datetime import datetime

# Create your models here.
class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50, default="")
    phone=models.IntegerField(default=0)
    description=models.CharField(max_length=1000, default="")
    otp=models.CharField(max_length=10, default="")
    

    def __str__(self):
        return self.name

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    pprname = models.CharField(max_length=100, default="")
    noofques = models.IntegerField(default=0)
    question = models.CharField(max_length=10000, default="")
    pprcode = models.CharField(max_length=50, default="")
    pprteach = models.CharField(max_length=100, default="")
    pdfop = models.CharField(max_length=10,default="")
    starttime = models.DateTimeField(default=datetime.now)
    endtime = models.DateTimeField(default=datetime.now)
    review=models.CharField(max_length=1000,default='')
    

    def __str__(self):
        return self.pprcode

class Student(models.Model):
    stuid = models.AutoField(primary_key=True)
    studname = models.CharField(max_length=100, default="")
    studemail = models.EmailField(max_length=100, default="")
    result = models.CharField(max_length=10000,default="")
    studrn = models.CharField(max_length=100,default="")
    pprcode = models.CharField(max_length=50, default="")
    studinst = models.CharField(max_length=500,default="")
    subtime = models.CharField(max_length=100,default="")
    pdf=models.FileField(upload_to="ansside/pdfs", max_length=100, default="")
    review = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.studemail
    
class Contact(models.Model):
    contactid = models.AutoField(primary_key=True)
    contactname = models.CharField(max_length=100, default="")
    contactemail = models.CharField(max_length=100, default="")
    contactmsg = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.contactemail