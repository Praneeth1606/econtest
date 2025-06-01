from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SignupForm
from .forms import LoginForm
from .models import Participant
from .models import Result
from .models import Submission
from datetime import datetime, timedelta, timezone
from app.qnEvaluate import score
import re
import decimal
import threading
import pytz
ist = pytz.timezone("Asia/Kolkata")
# Create your views here.

pno = 0


startTime = ist.localize(datetime(2025,5,26,18,35,00)) #Datetimes in IST
endTime = ist.localize(datetime(2025,5,29,23,35,00))

def checkStartTime():
	currTime = datetime.now(ist)
	if(currTime<startTime):
		return 1
	return 0

def checkEndTime():
	currTime = datetime.now(ist)
	if(currTime>endTime):
		return 1
	return 0

def returnRemTime():
	return int((endTime - datetime.now(ist)).total_seconds())

def setRemTime(request):
	Participant.objects.filter(username=request.session['username']).update(rem_time=returnRemTime())
	return


def disconnect_user(request): #check this
    
    if request.session.has_key('username'):
        usr = Participant.objects.get(name = request.session['username'])
        usr.rem_time = returnRemTime()
        usr.done = True
        usr.save()
    request.session.flush()
		
    


def index_view(request) :
	try:
		request.session['username']
	except KeyError:
		return redirect("login")
	return redirect("dashboard")


def register_view(request):
    if 'username' in request.session:
        return redirect("dashboard")
    
    error = None
    form1 = SignupForm(request.POST or None)
    if checkEndTime():
        disconnect_user(request)
        error = "Contest ended at UTC " + endTime.strftime("%H:%M:%S %d/%m/%Y")
        return standings_view(request, error)
    if form1.is_valid():
        form1.save()
        form1 = SignupForm()
        return redirect("login")
    elif form1.errors:
        error = "username already exists"
        # error = form1.error_messages
    context = {
        'form': form1,
        'error' : error
    }
    return render(request, "register.html", context)
        



def login_view(request):
    if 'username' in request.session:
        return redirect("dashboard")
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        error = None

        if checkStartTime():
            error = "You're early. The contest starts at IST " + startTime.strftime("%H:%M:%S %d/%m/%Y")
            return render(request, 'login.html', {'form':form, 'error':error})

        if checkEndTime():
            disconnect_user(request)
            error = "Contest ended at IST " + endTime.strftime("%H:%M:%S %d/%m/%Y") 
            return standings_view(request, error)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is None:
                error = 'Username or Password Incorrect'
            else:
                if user.done == True :
                    error = "Already Completed the Contest"
                else :
                    login(request, user)
                    request.session.modified = True
                    request.session['username'] = user.username
                    request.session['time'] = returnRemTime()
                    request.session.set_expiry(timedelta(hours=6).total_seconds())
                    return render(request, "index.html", {'rem_time': returnRemTime()})
                    
            return render(request, "login.html", {'form':form, 'error':error})

    form = LoginForm()
    return render(request, "login.html", {'form': form})

def dashboard_view(request):
    if 'username' in request.session:
        setRemTime(request)

        if checkEndTime():
            disconnect_user(request)
            error = "Contest ended at IST " + endTime.strftime(
                "%H:%M:%S %d/%m/%Y")
            return standings_view(request, error)
        
    
        if request.method == 'POST' and ('quit' in request.POST or 'remTime' in request.POST):
            user = Participant.objects.get(username = request.session['username'])
            user.done = True
            user.rem_time = request.POST.get('remTime', None)
            user.save()
            request.session.flush()
            return redirect("login")
        
        elif (request.method == 'POST' and 'code' in request.POST) :
            setRemTime(request)
            if checkEndTime():
                disconnect_user(request)
                error = "Contest ended at IST " + endTime.strftime(
                    "%H:%M:%S %d/%m/%Y")
                return standings_view(request, error)
            user = Participant.objects.get(username=request.session['username']) 
            if not Result.objects.filter(user = user).exists():
                res = Result(user = user)
                res.save()
            CODE = request.POST.get('code')
            qn = str(request.POST.get('question-select'))
            initTime = returnRemTime()

            res = 'Nothing yet'

            def evaluate(code,qn,init_time) : 
                global pno
                qn_no = str(re.sub('[^0-9]+',"",str(qn)))
                res = score(code,qn_no,str(pno))

                currRes = Result.objects.get(user = user)
                if (res == 'CORRECT ANSWER'):
                    messages.success(request, res)
                    if (qn == 'QN1'):
                        if currRes.q1s == 100:
                            currRes.q1t = min([currRes.q1t, init_time])
                        elif currRes.q1s == None or currRes.q1s < 100:
                            currRes.q1s = 100
                            currRes.q1t = init_time
                    elif (qn == 'QN2'):
                        if currRes.q2s == 100:
                            currRes.q2t = min([currRes.q2t, init_time])
                        elif currRes.q2s == None or currRes.q2s < 100:
                            currRes.q2s = 100
                            currRes.q2t = init_time
                    elif (qn == 'QN3'):
                        if currRes.q3s == 100:
                            currRes.q3t = min([currRes.q3t, init_time])
                        elif currRes.q3s == None or currRes.q3s < 100:
                            currRes.q3s = 100
                            currRes.q3t = init_time
                    elif (qn == 'QN4' ):
                        if currRes.q4s == 100:
                            currRes.q4t = min([currRes.q4t, init_time])
                        elif currRes.q4s == None or currRes.q4s < 100:
                            currRes.q4s = 100
                            currRes.q4t = init_time
                    elif (qn == 'QN5'):
                        if currRes.q5s == 100:
                            currRes.q5t = min([currRes.q5t, init_time])
                        elif currRes.q5s == None or currRes.q5s < 100:
                            currRes.q5s = 100
                            currRes.q5t = init_time
                    elif (qn == 'QN6'):
                        if currRes.q6s == 100:
                            currRes.q6t = min([currRes.q6t, init_time])
                        elif currRes.q6s == None or currRes.q6s < 100:
                            currRes.q6s = 100
                            currRes.q6t = init_time
                    elif (qn == 'QN7'):
                        if currRes.q7s == 100:
                            currRes.q7t = min([currRes.q7t, init_time])
                        elif currRes.q7s == None or currRes.q7s < 100:
                            currRes.q7s = 100
                            currRes.q7t = init_time
                    elif (qn == 'QN8'):
                        if currRes.q8s == 100:
                            currRes.q8t = min([currRes.q8t, init_time])
                        elif currRes.q8s == None or currRes.q8s < 100:
                            currRes.q8s = 100
                            currRes.q8t = init_time
                    
                    submis = Submission(user=user, mark=100, message=res, timeofs=str(timedelta(seconds=float(init_time))), qnno=int(qn_no))
                else:
                    messages.success(request, res)
                    if (qn == 'QN1'):
                        currRes.q1s = currRes.q1s if currRes.q1s is not None else 0
                    elif (qn == 'QN2'):
                        currRes.q2s = currRes.q2s if currRes.q2s is not None else 0
                    elif (qn == 'QN3'):
                        currRes.q3s = currRes.q3s if currRes.q3s is not None else 0
                    elif (qn == 'QN4'):
                        currRes.q4s = currRes.q4s if currRes.q4s is not None else 0
                    elif (qn == 'QN5'):
                        currRes.q5s = currRes.q5s if currRes.q5s is not None else 0
                    elif (qn == 'QN6'):
                        currRes.q6s = currRes.q6s if currRes.q6s is not None else 0
                    elif (qn == 'QN7'):
                        currRes.q7s = currRes.q7s if currRes.q7s is not None else 0
                    elif (qn == 'QN8'):
                        currRes.q8s = currRes.q8s if currRes.q8s is not None else 0
                    submis = Submission(user = user,mark = 0,message = res,timeofs=str(timedelta(seconds=float(init_time))),qnno = int(qn_no))

                submis.save()

                scorel = [currRes.q1s,currRes.q2s,currRes.q3s,currRes.q4s,currRes.q5s,currRes.q6s,currRes.q7s,currRes.q8s]
                timel = [currRes.q1t,currRes.q2t,currRes.q3t,currRes.q4t,currRes.q5t,currRes.q6t,currRes.q7t,currRes.q8t]
                pno += 1
                currRes.tot_score = sum([e for e in scorel if e is not None])
                currRes.tot_time = sum([decimal.Decimal(e) for e in timel if e is not None])
                user.rem_time = int((endTime-startTime).total_seconds()) - init_time
                currRes.save()
                user.save()
            threading.Thread(target = evaluate,args = (CODE,qn,int((endTime-startTime).total_seconds())-initTime)).start()
            messages.success(request, "Your submission was successful!")
            return redirect("dashboard")
        user = Participant.objects.get(username = request.session['username'])
        rem_time = user.rem_time
        if rem_time > 0 :
            return render(request, 'index.html',{'name' : request.session['username'],'rem_time' : rem_time})
        else :
            
            user.done = True
            user.save()
            request.session.flush()
            return redirect("login")
    else:
        return redirect("login")
    
def standings_view(request, error = None) :
    res = Result.objects.order_by("-tot_score","tot_time")
    return render(request, 'standings.html',{'results' : res, 'error' : error})

def submissions_view(request) :
    if 'username' in request.session:
        if checkEndTime():
            disconnect_user(request)
            error = "Contest ended at IST " + endTime.strftime(
                "%H:%M:%S %d/%m/%Y")
            return standings_view(request, error)
        usr = Participant.objects.get(username = request.session['username'])
        subs = usr.submission.all()
        return render(request, 'submissions.html',{'name' : request.session['username'],'submissions' : subs})
    else:
        return redirect("login")
	
