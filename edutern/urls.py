from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',index),
    path('aboutus/',aboutus),
    path('blog/',blog),
    path('contact/',contact),
    path('coursedetails/',coursedetails),
    path('courses/',courses),
    path('elements/',elements),
    path('singleblog/',singleblog),
    path('saveuser/',saveuser),
    path('resendotp/',resendotp),
    path('verify/',verifyuser),
    path('checklogin/',checklogin),
    path('userdashboard/',userdashboard),
    path('courseplayer/',courseplayer),

    path('adminindex/',adminindex),
    path('adminlogin/',adminlogin),
    path('admincodorderlist/',admincodorderlist),
    path('adminlogincheck/',adminlogincheck),
    path('adminaddcourse/',adminaddcourse),
    path('adminsavecourse/',adminsavecourse),
    path('admincourselist/',admincourselist),
    path('adminaddlectures/',adminaddlectures),
    path('adminlectureslist/',adminlectureslist),
    path('adminuserslist/',adminuserslist),
    path('adminactiveusers/',adminactiveusers),
    path('admindeactiveusers/',admindeactiveusers),
    
    path('login/',login),
    path('registration/',registration),
    path('forget_password/',forget_password),
    path('editUserDetail/',editUserDetail),
    path('editPassword/',editPassword),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)