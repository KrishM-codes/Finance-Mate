import hashlib

#sign up
def register_user(db, cursor, username, password, email=None):
    cursor.reset()
    q="select*from users where username= '{}'".format(username)
    cursor.execute(q)
    x=cursor.fetchall()
    if(len(x)>0):
        return False
    else:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("INSERT INTO Users (Username, Password, Email) VALUES (%s, %s, %s)", (username, hashed_password, email))
        db.commit()
        return True

# User login function
def login_register(cursor, username, password):
    cursor.reset()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM Users WHERE Username = %s AND Password = %s", (username, hashed_password))
    user = cursor.fetchone()
    if(user):
        return True
    return False

def get_username(cursor,uname):
    cursor.reset()
    cursor.execute("SELECT Username FROM Users")
    names = cursor.fetchall()
    # print(names)
    for i in names:
        if(uname in i):
            return True
    return False


def addbudget(cursor,con,category, user, budgetlimit):
    cursor.reset()
    desc=""
    q1= "select*from users where username='{}'".format(user,)
    cursor.execute(q1)
    userinfo= cursor.fetchall()
    uid= userinfo[0][0]
    cursor.execute("select * from budgetcategories where category = '"+category+"'")
    cat = cursor.fetchall()
    if(len(cat)>0):
        return False
    q2= "select*from budgetcategories"
    cursor.execute(q2)
    bud= cursor.fetchall()
    budid=0
    if len(bud)==0:
        budid=1
    else:
        budid= (bud[len(bud)-1][0]) +1
    q3= "insert into budgetcategories values ({},{},'{}',{})".format(budid, uid, category, budgetlimit)
    cursor.execute(q3)
    con.commit()
    return True
    # print("data added successfully")


def addexpense(cursor,con,category, amt, date, desc, user):
    cursor.reset()
    new=0
    q1= "select*from users where username='{}'".format(user,)
    cursor.execute(q1)
    userinfo= cursor.fetchall()
    uid= userinfo[0][0]
    q2= "select*from budgetcategories where category= '{}'".format(category,)
    cursor.execute(q2)
    catinfo= cursor.fetchall()
    # print(catinfo)
    if(not(catinfo)):
        addbudget(cursor,con,category,user,0)
        q2= "select*from budgetcategories where category= '{}'".format(category,)
        cursor.execute(q2)
        catinfo= cursor.fetchall()
        new= 1
    
    catid = catinfo[0][0]
    q3= "select*from expenses"
    cursor.execute(q3)
    exp= cursor.fetchall()
    expid=0
    if len(exp)==0:
        expid=1
    else:
        expid= (exp[len(exp)-1][0]) +1
    q4= "insert into expenses values ({},{},{},'{}',{},'{}','{}')".format(expid, uid, catid, category, amt, date, desc)
    cursor.execute(q4)
    con.commit()
    # print("data added successfully")
    return new


def addincome(cursor,con,income, amt, date, desc, user):
    cursor.reset()
    q1= "select*from users where username='{}'".format(user,)
    cursor.execute(q1)
    userinfo= cursor.fetchall()
    uid= userinfo[0][0]
    q2= "select*from income"
    cursor.execute(q2)
    inc= cursor.fetchall()
    incid=0
    if len(inc)==0:
        incid=1
    else:
        incid= (inc[len(inc)-1][0]) +1
    q3= "insert into income values ({},{},'{}',{},'{}','{}')".format(incid, uid, income, amt, date, desc)
    cursor.execute(q3)
    con.commit()
    # print("data added successfully")

def updateexpense(cursor,con,expid, infolist,uname):
    cursor.reset()
    q1= "delete from expenses where expenseid='{}'".format(expid,)
    cursor.execute(q1)
    #infolist= (expenseid,userid,categoryid,category,amount,date,description)
    addexpense(cursor,con,infolist[3],infolist[4],infolist[5],infolist[6],uname)
    con.commit()
    return True

def updatebudget(cursor,con,catid, infolist,uname):
    cursor.reset()
    q1= "delete from budgetcategories where categoryid='{}'".format(catid,)
    cursor.execute(q1)
    #infolist= (category, budgetlimit)
    addbudget(cursor,con,infolist[0],uname,infolist[1])

    cursor.execute("update expenses set categoryid = (select categoryid from budgetcategories where category = '"+ infolist[0] +"') ")
    con.commit()
    return True

def updateincome(cursor,con,incid, infolist,uname):
    cursor.reset()
    q1= "delete from income where incomeid='{}'".format(incid,)
    cursor.execute(q1)
    #infolist= (source, ammount, date, description)
    addincome(cursor,con,infolist[0],infolist[1],infolist[2],infolist[3],uname)
    con.commit()
    return True


def deleteexpenses(cursor, con, expid):
    cursor.reset()
    q3="delete from expenses where expenseid={}".format(expid,)
    cursor.execute(q3)
    con.commit()
    return True

def deletebudget(cursor, con, catid):
    cursor.reset()
    q3="delete from budgetcategories where categoryid={}".format(catid,)
    cursor.execute(q3)
    con.commit()
    return True

def deleteincome(cursor, con, incid): 
    cursor.reset()
    q1="delete from income where incomeid='{}'".format(incid,)
    cursor.execute(q1)
    con.commit()
    return True


def readexpenseall(cursor,uname):
    cursor.reset()
    q1="select * from expenses where userid = (select userid from users where username = '"+uname+"') order by date desc"
    cursor.execute(q1)
    info= cursor.fetchall()
    print(info)
    return info

def readincomeall(cursor,uname):
    cursor.reset()
    q1="select*from income where userid = (select userid from users where username = '"+uname+"')order by date desc"
    cursor.execute(q1)
    info= cursor.fetchall()
    return info

def readbudgetall(cursor,uname):
    cursor.reset()
    q1="select*from budgetcategories where userid = (select userid from users where username = '"+uname+"')"
    cursor.execute(q1)
    info= cursor.fetchall()
    return info

def readusersall(cursor,uname):
    q1="select*from users where userid = (select userid from users where username = '"+uname+"')"
    cursor.execute(q1)
    info= cursor.fetchall()
    return info

def recentexpense(cursor,uname):
    q1="select * from expenses where userid = (select userid from users where username = '"+uname+"') order by date desc"
    cursor.execute(q1)
    info = cursor.fetchmany(5)
    return info

def categoryexpenses(cursor,uname):
    q1 = "select sum(Amount), category from expenses where userid =(select userid from users where username = '"+uname+"')"
    q1 += "group by category"
    cursor.execute(q1)
    info = cursor.fetchall()
    return info
