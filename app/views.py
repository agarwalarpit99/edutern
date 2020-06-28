from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.decorators.csrf import *
from app.models import *
from django.core.paginator import *
from django.core.mail import EmailMessage
from django.http import HttpResponse
import uuid
from app.myutil import *
import csv
from datetime import date

# Create your views here.
def index(request):
	return render(request,'index.html',{})
def aboutus(request):
	return render(request,'about-us.html',{})
def blog(request):
	return render(request,'blog.html',{})
def contact(request):
	return render(request,'contact.html',{})
def coursedetails(request):
	return render(request,'course-details.html',{})
def courses(request):
	return render(request,'courses.html',{})
def elements(request):
	return render(request,'elements.html',{})
def singleblog(request):
	return render(request,'single-blog.html',{})
def adminlogin(request):
	return render(request,'adminpages/login.html',{})
def admincodorderlist(request):
	return render(request,'adminpages/codorderlist.html',{})
def login(request):
	return render(request,'login.html',{})
def registration(request):
	return render(request,'registration.html',{})
@csrf_exempt
def saveuser(request):
	if request.method=='POST':
		fname=request.POST.get('fname')
		lname=request.POST.get('lname')
		email=request.POST.get('email')
		mobile=request.POST.get('mobile')
		password=request.POST.get('password')
		obj=UserData.objects.all().delete()
		u="U00"
		x=1
		uid=u+str(x)
		while UserData.objects.filter(User_ID=uid).exists():
			x=x+1
			uid=u+str(x)
		x=int(x)
		otp=uuid.uuid5(uuid.NAMESPACE_DNS, date.today().strftime("%d/%m/%Y")+uid+fname+lname+password+mobile+email).int
		otp=str(otp)
		otp=otp.upper()[0:6]
		request.session['userotp'] = otp
		obj=UserData(
			Join_Date=date.today().strftime("%d/%m/%Y"),
			User_ID=uid,
			User_FName=fname,
			User_LName=lname,
			User_Email=email,
			User_Phone=mobile,
			User_Password=password
			)
		if UserData.objects.filter(User_Email=email).exists():
			return HttpResponse("<script>alert('User Already Exists'); window.location.replace('/registration/')</script>")
		else:
			obj.save()
			msg='''Hi there!
Please verify your account with the following One Time Password

Verification OTP : '''+otp+'''

Thanks for creating your account on Edutern,
Team Edutern'''
			sub='Edutern One Time Password (OTP)'
			email=EmailMessage(sub,msg,to=[email])
			email.send()
			return render(request,'verify.html',{'userid':uid})
@csrf_exempt
def verifyuser(request):
	if request.method=='POST':
		otp=request.POST.get('otp')
		uid=request.POST.get('uid')
		if request.session['userotp'] == otp:
			request.session['userid'] = uid
			return HttpResponse("<script>alert('Account Created Successfully!'); window.location.replace('/userdashboard/')</script>")
		else:
			dic={'msg':'Incorrect OTP', 'userid':uid}
			return render(request,'verify.html',dic)
	else:
		return HttpResponse('<h1>400 Page Not Found</h1>')
def resendotp(request):
	uid=request.GET.get('uid')
	otp=request.session['userotp']
	email=''
	for x in UserData.objects.filter(User_ID=uid):
		email=x.User_Email
	msg='''Hi there!
Please verify your account with the following One Time Password

Verification OTP : '''+otp+'''

Thanks for creating your account on Edutern,
Team Edutern'''
	sub='Edutern One Time Password (OTP)'
	email=EmailMessage(sub,msg,to=[email])
	email.send()
	dic={'msg':'OTP Sent', 'userid':uid}
	return render(request,'verify.html',dic)
@csrf_exempt
def checklogin(request):
	if request.method=='POST':
		email=request.POST.get('email')
		password=request.POST.get('password')
		if UserData.objects.filter(User_Email=email,User_Password=password).exists():
			for x in UserData.objects.filter(User_Email=email,User_Password=password):
				request.session['userid']=x.User_ID
			return redirect('/userdashboard/')
		else:
			return HttpResponse("<script>alert('Incorrect Credentials'); window.location.replace('/login/')</script>")
def userdashboard(request):
	return render(request,'userdashboard.html',{})

@csrf_exempt
def adminlogincheck(request):
	if request.method=='POST':
		email=request.POST.get('email')
		password=request.POST.get('password')
		if email == 'admin@edutern.in' and password == '1234':
			request.session['adminid'] = email
			return redirect('/adminindex/')
		else:
			return HttpResponse("<script>alert('Incorrect Credentials'); window.location.replace('/adminlogin/')</script>")
	else:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def adminindex(request):
	try:
		adminid=request.session['adminid']
		return render(request,'adminpages/index.html',{})
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def adminaddcourse(request):
	try:
		adminid=request.session['adminid']
		return render(request,'adminpages/addcourse.html',{})
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
@csrf_exempt
def adminsavecourse(request):
	try:
		adminid=request.session['adminid']
		if request.method=='POST':
			name=request.POST.get('name')
			trainer=request.POST.get('trainer')
			fee=request.POST.get('fee')
			objective=request.POST.get('objective')
			eligibility=request.POST.get('eligibility')
			contents=request.POST.get('content')
			thumbnail=request.FILES['thumbnail']
			c="CRS00"
			x=1
			cid=c+str(x)
			while CourseData.objects.filter(Course_ID=cid).exists():
				x=x+1
				cid=c+str(x)
			x=int(x)
			obj=CourseData(
				Course_ID=cid,
				Course_Name=name,
				Course_Trainer=trainer,
				Course_Fee=fee,
				Course_Objective=objective,
				Course_Eligibility=eligibility,
				Course_Content=contents,
				Course_Thumb=thumbnail
				)
			if CourseData.objects.filter(Course_Name=name).exists():
				return HttpResponse("<script>alert('Course Already Exists'); window.location.replace('/adminaddcourse/')</script>")
			else:
				obj.save()
				return HttpResponse("<script>alert('Course Added Successfully'); window.location.replace('/adminaddcourse/')</script>")
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def admincourselist(request):
	try:
		adminid=request.session['adminid']
		dic={'data':CourseData.objects.all()}
		return render(request,'adminpages/courselist.html',dic)
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def userdashboard(request):
	return render(request,'userdashboard.html',{})
def courseplayer(request):
	return render(request,'courseplayer.html',{})
def adminaddlectures(request):
	return render(request,'adminpages/addlectures.html',{})
def adminlectureslist(request):
	return render(request,'adminpages/lectureslist.html',{})
def adminuserslist(request):
	return render(request,'adminpages/userslist.html',{})
def adminactiveusers(request):
	return render(request,'adminpages/activeusers.html',{})
def admindeactiveusers(request):
	return render(request,'adminpages/deactiveusers.html',{})
