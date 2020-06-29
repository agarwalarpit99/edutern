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
from .myutil import *

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
	course_id=request.GET.get('course_id')
	if CourseData.objects.filter(Course_ID=course_id).exists():
		course_data=CourseData.objects.filter(Course_ID=course_id)
		lecture_data=LecturesData.objects.filter(Course_ID=course_id).all()

		return render(request,'course-details.html',{'course_data':course_data,'lecture_data':lecture_data})
	else:
		return HttpResponse("<h1>Course not found")
def courses(request):
	if check_user:
		course_data=CourseData.objects.all()
		return render(request,'courses.html',{'course_data':course_data})
	else:
		return HttpResponse("<h1>Course not found")

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
	if check_user:
		uid=request.session['userid']
		data=UserData.objects.filter(User_ID=uid).all()
	return render(request,'userdashboard.html',{'data':data})
def courseplayer(request):
	if check_user:
		lecture_id=request.GET.get('lecture_id')
		course_id=request.GET.get('course_id')
		lecture_data=LecturesData.objects.filter(Lecture_ID=lecture_id)
		lecture_list=LecturesData.objects.filter(Course_ID=course_id).all()
		
		return render(request,'courseplayer.html',{'lecture_data':lecture_data,'lecture_list':lecture_list})
	else:
		return HttpResponse("not allowed")
def adminaddlectures(request):
	try:
		adminid=request.session['adminid']
		data=CourseData.objects.all()
		return render(request,'adminpages/addlectures.html',{'data':data})
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
@csrf_exempt
def adminsavelecture(request):
	if request.method=='POST':
		course=request.POST.get('course')
		name=request.POST.get('name')
		video=request.FILES['video']
		l="LEC00"
		x=1
		lid=l+str(x)
		while LecturesData.objects.filter(Lecture_ID=lid).exists():
			x=x+1
			lid=l+str(x)
		x=int(x)
		obj=LecturesData(
			Lecture_ID=lid,
			Course_ID=course,
			Lecture_Name=name,
			Lecture_Video=video
			)
		obj.save()
		return HttpResponse("<script>alert('Lecture Added Successfully'); window.location.replace('/adminaddlectures/')</script>")
	else:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def adminlectureslist(request):
	try:
		adminid=request.session['adminid']
		data=LecturesData.objects.all()
		return render(request,'adminpages/lectureslist.html',{'data':data})
	except:
		return HttpResponse('<h1>Error 404 : Page Not Found</h1>')
def adminuserslist(request):
	return render(request,'adminpages/userslist.html',{})
def adminactiveusers(request):
	return render(request,'adminpages/activeusers.html',{})
def admindeactiveusers(request):
	return render(request,'adminpages/deactiveusers.html',{})
def forget_password(request):
	if request.method=='POST':

		email=request.POST['email']
		if UserData.objects.filter(User_Email=email).exists():
			data=UserData.objects.filter(User_Email=email).values('User_Password')[0]['User_Password']
			sub='Your Account Password'
			
			email=EmailMessage(sub,data,to=[email])
			email.send()

			return HttpResponse("<script>alert('Your Password has been send to your mail'); window.location.replace('/login/')</script>")
	
		else:
			return HttpResponse("Email not exists ")

		uid=request.session['userid']
		password=''
		data=UserData.objects.filter(User_ID=uid)
		for x in data:
			password=x.User_Password
		sub='Edutern - Your Account Password'
		email=request.POST['email']
		msg='''Hi there!
Your Edutern Account Password is,

'''+password+'''

Thanks for creating your account on Edutern,
Team Edutern'''
		email=EmailMessage(sub,data,to=[email])
		email.send()
		return HttpResponse("<script>alert('Your Password has been send to your mail'); window.location.replace('/login/')</script>")
	else:
		return render(request,'forgot_password.html',{})
def editUserDetail(request):
	if request.method=='POST':
		uid=request.session['userid']
		user_data=UserData.objects.filter(User_ID=uid)
		for i in user_data:
			i.User_FName=request.POST['first_name']
			i.User_LName=request.POST['last_name']
			i.User_Phone=request.POST['phone']
			i.save()
			return HttpResponse("<script>alert('Congratulations !! Your details is SuccessFully Updated'); window.location.replace('/userdashboard/')</script>")
def editPassword(request):
	if request.method=='POST':
		uid=request.session['userid']
		user_data=UserData.objects.filter(User_ID=uid)
		old_pass=UserData.objects.filter(User_ID=uid).values('User_Password')[0]['User_Password']
		old_password=request.POST['old_password']
		if old_pass==old_password:
			for i in user_data:
				new_pass=int(request.POST['new_password'])
				i.User_Password=new_pass
				i.save()
				return HttpResponse("<script>alert('Congratulations !! Your Password is SuccessFully Updated'); window.location.replace('/userdashboard/')</script>")
		else:
			return HttpResponse("<script>alert('Pleasr check your old password'); window.location.replace('/userdashboard/')</script>")


