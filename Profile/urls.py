from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.profile, name="userprofile"),
    path('changes/',views.changepro, name="changepro"),
    path('allquestion/', views.allquestion, name="allquestion"),
    path('question/<str:code>/', views.questionview, name="quessubmission"),
    path('quesviewer/<str:code>/', views.quesviewer, name="questionsviewer"),
    path('deleteppr/<str:code>/', views.deleteppr, name="deleteppr"),
    path('norview/<str:email>/<str:code>/', views.norquesview, name="norquesview"),

]