from django.http import HttpResponse
from django.shortcuts import render
from .CRUD import *
import mysql.connector

# Establish connection to the database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database="FinanceMate"
)

# Create a cursor object to execute SQL queries


# Create your views here.
def home(request):
    return render(request,'App/home.html')

def login(request):
    global mydb
    cursor = mydb.cursor()
    status=0
    username=""
    if request.method == 'POST':
        username = (request.POST.get('logusername',''))
        passwd = (request.POST.get('logpass',''))
        # print(username,passwd)
        if(login_register(cursor,username,passwd)):
            status=1
        else:
            status=2
    
    cursor.close()

    context={"status":status,"username":username}
    return render(request,'App/login.html',context)

def signup(request):
    global mydb
    cursor = mydb.cursor()
    status=0
    uname=''
    if request.method == 'POST':
        username = (request.POST.get('logusername',''))
        passwd = (request.POST.get('logpass',''))
        confirmpasswd = (request.POST.get('confirmpass',''))
        email = (request.POST.get('email',''))
        if(passwd!=confirmpasswd):
            status = -1
        elif(register_user(mydb, cursor,username,passwd)):
            status = 1
            uname= str(username)
        else:
            status=2
    
    cursor.close()

    context={"status":status,'username':uname}
    return render(request,'App/signup.html',context)

fname,lname,email,profession="","","",""
def dashboard(request,uname):
    global mydb,fname,lname,email,profession

    cursor = mydb.cursor()
    isvalid=False
    data=[]
    if(get_username(cursor,uname)):
        isvalid=True
        data = recentexpense(cursor,uname)
        for i in data:  
            index = (data.index(i))
            i=list(i)
            i.append(index+1)
            data[index]=i
        
        data1 = readbudgetall(cursor,uname)
        for i in data1:  
            index = (data1.index(i))
            i=list(i)
            i.append(index+1)
            data1[index]=i
        
        data2 = categoryexpenses(cursor,uname)
        for i in data1:
            for j in data2:
                if(i[2]==j[1]):
                    i.append(j[0])
        
        if request.method =='POST':
            if request.POST.get('profileedit'):
                fname = (request.POST.get('firstName',''))
                lname = (request.POST.get('lastName',''))
                email = (request.POST.get('email',''))
                profession = (request.POST.get('profession',''))

    cursor.close()
    
    context={'isvalid':isvalid,'username':uname,'data':data,'data2':data1,'fname':fname,'lname':lname,'email':email,'profession':profession}
    return render(request,'App/dashboard.html',context)


def expenses(request,uname):
    global mydb

    cursor = mydb.cursor()
    editing,deleting=False,False
    index1=0
    category,amount,date,description = '',0,'',''
    listedit=[category,amount,date,description]
    data = readexpenseall(cursor,uname)
    for i in data:  
        index = (data.index(i))
        i=list(i)
        i.append(index+1)
        data[index]=i
    
    if request.method =='POST':
        if request.POST.get('add'):
            category = (request.POST.get('category',''))
            amount = float(request.POST.get('amount',''))
            date = (request.POST.get('date',''))
            description = (request.POST.get('description',''))

            # print(category,amount,date,description)
            addexpense(cursor,mydb,category,amount,date,description,uname)

        elif request.POST.get('edit'):
            editing=True
            index1 = int(request.POST.get('edit')) - 1
            category = data[index1][3]
            amount = data[index1][4]
            date = data[index1][5]
            description = data[index1][6]
            listedit=[category,amount,date,description]
            
        elif request.POST.get('editcancel'):
            editing=False

        elif request.POST.get('editsave'):
            index1 = int(request.POST.get('editsave'))
            category = (request.POST.get('category',''))
            amount = float(request.POST.get('amount',''))
            date = (request.POST.get('date',''))
            description = (request.POST.get('description',''))
            updateexpense(cursor,mydb,data[index1][0],[data[index1][0],data[index1][1],data[index1][2],category,amount,date,description],uname)

        elif request.POST.get('delete'):
            index1 = int(request.POST.get('delete')) - 1
            expid=data[index1][0]
            deleteexpenses(cursor,mydb,expid)
        
    data = readexpenseall(cursor,uname)
    for i in data:  
        index = (data.index(i))
        i=list(i)
        i.append(index+1)
        data[index]=i

    cursor.close()

    context={'username':uname,'data':data,'listedit':listedit,'editing':editing,'deleting':deleting,'index':index1}
    return render(request,'App/expenses.html',context)

def income(request,uname):
    global mydb

    cursor = mydb.cursor()
    editing,deleting=False,False
    index1=0
    Source,amount,date,description = '',0,'',''
    listedit=[Source,amount,date,description]
    data = readincomeall(cursor,uname)
    for i in data:  
        index = (data.index(i))
        i=list(i)
        i.append(index+1)
        data[index]=i
    print(data)
    if request.method =='POST':
        if request.POST.get('add'):
            Source = (request.POST.get('Source',''))
            amount = float(request.POST.get('amount',''))
            date = (request.POST.get('date',''))
            description = (request.POST.get('description',''))
            print(description)
            # print(Source,amount,date,description)
            addincome(cursor,mydb,Source,amount,date,description,uname)

        elif request.POST.get('edit'):
            editing=True
            index1 = int(request.POST.get('edit')) - 1
            Source = data[index1][2]
            amount = data[index1][3]
            date = data[index1][4]
            description = data[index1][5]
            listedit=[Source,amount,date,description]
            
        elif request.POST.get('editcancel'):
            editing=False

        elif request.POST.get('editsave'):
            index1 = int(request.POST.get('editsave'))
            Source = (request.POST.get('Source',''))
            amount = float(request.POST.get('amount',''))
            date = (request.POST.get('date',''))
            description = (request.POST.get('description',''))
            updateincome(cursor,mydb,data[index1][0],[Source,amount,date,description],uname)

        elif request.POST.get('delete'):
            index1 = int(request.POST.get('delete')) - 1
            expid=data[index1][0]
            deleteincome(cursor,mydb,expid)
        
    data = readincomeall(cursor,uname)
    for i in data:  
        index = (data.index(i))
        i=list(i)
        i.append(index+1)
        data[index]=i

    cursor.close()

    context={'username':uname,'data':data,'listedit':listedit,'editing':editing,'deleting':deleting,'index':index1}
    
    return render(request,'App/income.html',context)

def budget(request,uname):
    global mydb

    cursor = mydb.cursor()
    editing,deleting=False,False
    index1=0
    category,amount = '',0
    listedit=[category,amount]
    data = readbudgetall(cursor,uname)
    # print(data)
    for i in data:  
        index = (data.index(i))
        i=list(i)
        i.append(index+1)
        data[index]=i
    
    added=[True,category]
    if request.method =='POST':
        if request.POST.get('add'):
            category = (request.POST.get('category',''))
            amount = float(request.POST.get('amount',''))

            added=[False,category]
            # print(category,amount,date,description)
            if(addbudget(cursor,mydb,category,uname,amount)):
                added=[True,category]

        elif request.POST.get('edit'):
            editing=True
            print(index1)
            index1 = int(request.POST.get('edit')) - 1
            print(index1)
            category = data[index1][2]
            amount = data[index1][3]
            listedit=[category,amount]
            
        elif request.POST.get('editcancel'):
            editing=False

        elif request.POST.get('editsave'):
            index1 = int(request.POST.get('editsave'))
            category = (request.POST.get('category',''))
            amount = float(request.POST.get('amount',''))
            print(index1,data[index1][0])
            updatebudget(cursor,mydb,data[index1][0],[category,amount],uname)

        elif request.POST.get('delete'):
            index = int(request.POST.get('delete')) - 1
            budid=data[index1][0]
            deletebudget(cursor,mydb,budid)
        
    data = readbudgetall(cursor,uname)
    # print(data)
    for i in data:  
        index = (data.index(i))
        i=list(i)
        i.append(index+1)
        data[index]=i
    
    # data2 = categoryexpenses(cursor,uname)
    # for i in data:
    #     for j in data2:
    #         if(i[2]==j[1]):
    #             i.append(j[0])
    
    cursor.close()

    context={'username':uname,'data':data,'listedit':listedit,'editing':editing,'deleting':deleting,'index':index1,'added':added}

    return render(request,'App/budget.html',context)

def financialgoals(request,uname):
    context={'username':uname}
    return render(request,'App/financialgoals.html',context)