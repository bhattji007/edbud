from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="teachhome"),
    path('register', views.teachregister, name="teachregister"),
    path('logout/', views.logout, name="logout"),
    path('forgotpassword/', views.forgotpass, name="forgotpass"),
    path('norques/', views.norques, name="norques"),
    path('norques/<str:n>/<str:pn>/', views.norquesset, name="norquesset"),
    path('mcqques/', views.mcqques ,name="mcqques"),
    path('mcqques/<str:n>/<str:pn>/', views.mcqquesset, name="mcqquesset"),
    path('review/<str:code>/', views.teachreview, name="teachreview"),
    path('otpverify/<str:email>/', views.otpverification, name="otpverify"),
]