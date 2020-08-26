from django.contrib import admin
from .models import Teacher, Question, Student, Contact
# Register your models here.
admin.site.register(Teacher)
admin.site.register(Question)
admin.site.register(Student)
admin.site.register(Contact)