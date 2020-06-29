from django.db import models
from django.conf import settings
from datetime import date

class CourseData(models.Model):
	Course_ID=models.CharField(max_length=20, primary_key=True)
	Course_Name=models.CharField(max_length=100)
	Course_Trainer=models.CharField(max_length=100)
	Course_Fee=models.CharField(max_length=50)
	Course_Objective=models.CharField(max_length=1000)
	Course_Eligibility=models.CharField(max_length=1000)
	Course_Thumb=models.FileField(upload_to='coursethumb/')
	class Meta:
		db_table="CourseData"

class LecturesData(models.Model):
	Lecture_ID=models.CharField(max_length=20, primary_key=True)
	Course_ID=models.CharField(max_length=20)
	Lecture_Name=models.CharField(max_length=100)
	Lecture_Video=models.FileField(upload_to='courselectures/')
	class Meta:
		db_table="LecturesData"

class UserData(models.Model):
	Join_Date=models.CharField(max_length=50, default=date.today().strftime("%d/%m/%Y"))
	User_ID=models.CharField(max_length=20, primary_key=True)
	User_FName=models.CharField(max_length=50)
	User_LName=models.CharField(max_length=50)
	User_Email=models.CharField(max_length=70)
	User_Phone=models.CharField(max_length=15)
	User_Password=models.CharField(max_length=20)
	Verify_Status=models.CharField(max_length=12, default='Unverified')
	Status=models.CharField(max_length=10, default='Active')
	class Meta:
		db_table="UserData"