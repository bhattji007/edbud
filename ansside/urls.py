from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="anshome"),
    path('mcq/<str:code>/<str:email>',views.mcqpapercenter, name="mcqpapercenter"),
    path('normal/<str:code>/<str:email>',views.normalpapercenter, name="normalpapercenter"),
    path('normal/pdf/<str:code>/<str:email>/', views.anspdf, name="anspdf"),
    path('review/<str:code>/<str:email>/', views.review, name="review")
]