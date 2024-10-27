from django.urls import path
from pathoapp import views  # Importing all views
#from .views import viewurine, deleteurine, updateurine  # Explicitly importing specific views
#from .urinepdfreport import generate_urine_test_report  # Import the report generation function
from .views import generate_haematology_report  # Import the function from views
from django.urls import path
from .views import UserLoginView, home
from django.contrib.auth import views as auth_views

from .views import UserPasswordChangeView
from django.contrib.auth import views as auth_views




urlpatterns = [ 
    path('', home, name='home'),  # This sets the home view as the root URL 
              
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  
    path('register/', views.register, name='register'),  # Register URL
    
    path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
                
    path('about/', views.About, name='about'),
    path('contact/', views.Contact, name='contact'),
   
    path('adddoctor/', views.adddoctor, name='adddoctor'),
    path('delete/<str:doctorname>/', views.deletedoctor, name='deletedata'),
    path('get-doctor-email/', views.get_doctor_email, name='get_doctor_email'),  # URL for fetching doctor email
    
    path('addpatient/', views.addpatient, name='addpatient'),
    path('get_patient_data/', views.get_patient_data, name='get_patient_data'),
    path('viewpatient/', views.viewpatient, name='viewpatient'),
    path('updatepatient/<int:patientid>', views.updatepatient, name='updatepatient'),
    path('deletepatient/<int:patientid>', views.deletepatient, name='deletepatient'),
    
    path('addhaematolgy/', views.addhaematology, name='addhaematology'),
    path('viewhaematology/', views.viewhaematology, name='viewhaematology'),
    path('updatehaematology/<str:test_id>/', views.updatehaematology, name='updatehaematology'),
    path('deletehaematology/<str:test_id>/', views.deletehaematology, name='deletehaematology'),
    path('haematology_report/<int:test_id>/', generate_haematology_report, name='generate_haematology_report'),
    
    path('test1/', views.handle_test1_submission, name='test1'),
    path('test2/', views.handle_test2_submission, name='test2'),
    path('test3/', views.handle_test3_submission, name='test3'),
    #path('test2/', views.handle_test2_submission, name='test2'),
    path('', views.Index, name='home'),
    
    #path('addurine/', views.addurine, name='addurine'),
    #path('deleteurine/<str:testid>/', views.deleteurine, name='deleteurine'),
    #path('updateurine/<str:testid>/', views.updateurine, name='updateurine'),
    #path('viewurine/', views.viewurine, name='viewurine'),
    
    
    path('send-pdf/', views.send_pdf_via_email, name='send_pdf_via_email'),
    #path('urine-test-report/<int:testid>/', generate_urine_test_report, name='urine_test_report'),  # URL for the report
    path('addbloodsugar/', views.addbloodsugar, name='addbloodsugar'),
]