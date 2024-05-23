from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('',views.home,name='Home'),
    path('LogIn',views.login,name='login'),
    path('SignUp',views.signup,name='signup'),
    path('dashboard/<str:uname>/',views.dashboard,name='dashboard'),
    path('<str:uname>/expenses/',views.expenses,name='expenses'),
    path('<str:uname>/income/',views.income,name='income'),
    path('<str:uname>/budget/',views.budget,name='budget'),
    path('<str:uname>/financial-goals/',views.financialgoals,name='financial-goals'),

]
