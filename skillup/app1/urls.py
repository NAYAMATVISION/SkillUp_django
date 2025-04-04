from django.contrib import path
from . import views
urlpatterns = [
    path("",views.home),
    path("signup/",views.signup),
    path("login/",views.login),
    path("forgetPassword/",views.foget_password),
    path("dashboard/",views.dashboard),
    path("admindashboard/",views.is_admin),
    path("createcourse/",views.create_course),
    path("delete-course/<int:id>/" , views.delete_course),
    path("edit-course/<int:id>/", views.edit_course),
    path("courses/", views.courses),  
    path("course/", views.course),  
    path("terms-and-conditions/", views.terms),  
    path("profile/", views.profile),
    path("fullstack/", views.fullstack), 
    path("datascience/", views.datascience),  
    path("aiml/", views.AIML),  
    path("checkout/", views.checkout),
    
    

]


