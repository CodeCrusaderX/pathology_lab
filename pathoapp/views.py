from django.shortcuts import render,redirect, HttpResponseRedirect, get_object_or_404
from . models import *
from django.http import HttpResponse
from .forms import *
from django.contrib import messages
from django.http import JsonResponse

from django.db.models import Max
import os
from django.core.mail import EmailMessage # email pdf
from django.conf import settings
from io import BytesIO  #email pdf 
from django.http import FileResponse

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter #email pdf 
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse


from django.core.mail import send_mail  #checkbox email

from django.contrib.auth.views import LoginView   #login page 
from django.urls import reverse_lazy  # login page

from django.contrib.auth.views import PasswordChangeView   #changepass
from django.contrib.messages.views import SuccessMessageMixin  #changepass
#from .urinepdfreport import generate_urine_test_report
from django.contrib.auth.decorators import login_required
# views.py

from django.contrib.auth.forms import UserCreationForm  #signup


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # Redirect to the login page after registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def home(request):
    return render(request, 'home.html')


class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')  # Replace 'home' with the name of your homepage URL



class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('password_change_done')
    success_message = "Your password was successfully changed."



def About(request):
    return render(request,'about.html')

def Contact(request):
    return render(request,'contact.html')

def Index(request):
    return render(request,'index.html')




# View to add a new doctor
def adddoctor(request):
    if request.method == 'POST':
        fm = DoctorForm(request.POST)
        if fm.is_valid():
           fm.save()
        messages.add_message(request, messages.SUCCESS, 'Data Saved Successfully !!!')
        fm = DoctorForm() #data save hone ke baad phir se blank form aa jaye isliye
            
    else:
        fm = DoctorForm()
    doctor = Doctor.objects.all()
    return render(request, 'adddoctor.html',{'form':fm, 'doc':doctor})

def deletedoctor(request, doctorname):  # Accept 'doctorname' as a parameter
    if request.method == 'POST':
        Doctor.objects.filter(doctorname=doctorname).delete()  # Filter by doctorname and delete
        messages.add_message(request, messages.SUCCESS, 'Doctor Deleted Successfully !!!')
    return redirect('adddoctor')  # Redirect to 'adddoctor' page after deletion




def get_doctor_email(request):
    doctor_name = request.GET.get('doctorname', None)  # Get doctorname from AJAX request

    if doctor_name:
        try:
            doctor = Doctor.objects.get(doctorname=doctor_name)  # Fetch doctor by name
            return JsonResponse({'email': doctor.email})  # Return email in JSON format
        except Doctor.DoesNotExist:
            return JsonResponse({'email': ''})  # Return empty string if doctor does not exist
    return JsonResponse({'email': ''})


def addpatient(request):
    doctors = Doctor.objects.all()  # Fetch all doctors for dropdown

    if request.method == 'POST':
        patientid = request.POST['patientid']
        patientname = request.POST['patientname']
        age = request.POST['age']
        gender = request.POST['gender']
        mobile = request.POST['mobile']
        email = request.POST['email']
        address = request.POST['address']
        recondate = request.POST['recondate']
        doctor_name = request.POST['refbydoctor']  # Get selected doctor from dropdown

        try:
            # Fetch doctor instance by doctorname (since it's the primary key)
            doctor = Doctor.objects.get(doctorname=doctor_name)

            # Create a new PatientMaster record
            PatientMaster.objects.create(
                patientid=patientid,
                patientname=patientname,
                age=age,
                gender=gender,
                mobile=mobile,
                email=email,
                address=address,
                recondate=recondate,
                refbydoctor=doctor  # Save doctor reference
            )
            messages.success(request, 'Patient added successfully!')
            return redirect('viewpatient')  # Redirect to view patient after saving
        except Doctor.DoesNotExist:
            messages.error(request, 'Selected doctor does not exist.')
            return render(request, 'addpatient.html', {'error': 'yes', 'doctors': doctors})
        except Exception as e:
            messages.error(request, 'Something went wrong, please try again.')
            return render(request, 'addpatient.html', {'error': 'yes', 'doctors': doctors})

    return render(request, 'addpatient.html', {'doctors': doctors, 'error': 'no'})

def viewpatient(request):
    # Fetch all patient records including related doctor details
    patients = PatientMaster.objects.select_related('refbydoctor').all()

    # Pass the patient data to the template
    context = {
        'patients': patients
    }
    return render(request, 'viewpatient.html', context)

def deletepatient(request, patientid):
       # Get the patient object, or return a 404 if not found
    patient_data = get_object_or_404(PatientMaster, patientid=patientid)

    if request.method == 'POST':
        # Delete the patient record
        patient_data.delete()
        messages.success(request, "Record deleted successfully!")
        return redirect('viewpatient')
    return redirect('viewpatient')

    # Render a confirmation template or redirect as needed
    return redirect('view_patient')





def updatepatient(request, patientid):
    # Get the patient instance
    patient = get_object_or_404(PatientMaster, patientid=patientid)
    doctors = Doctor.objects.all()  # Fetch all doctors for dropdown

    if request.method == 'POST':
        # Update patient data from form
        patient.patientname = request.POST['patientname']
        patient.recondate = request.POST['recondate']
        patient.age = request.POST['age']
        patient.gender = request.POST['gender']
        patient.mobile = request.POST['mobile']
        patient.email = request.POST['email']
        patient.address = request.POST['address']
        doctor_name = request.POST['refbydoctor']
        patient.refbydoctor = get_object_or_404(Doctor, doctorname=doctor_name)

        try:
            patient.save()  # Save updated patient information
            messages.success(request, 'Patient updated successfully!')
            return redirect('viewpatient')  # Redirect back to the view patient page
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    # Render the update form with patient and doctor data
    return render(request, 'updatepatient.html', {'patient': patient, 'doctors': doctors})



# Your existing imports here...

# View to add Haematology Test
def addhaematology(request):
    # Get the next test ID for the Haematology test
    max_test_id = Haematology.objects.aggregate(Max('test_id'))['test_id__max']
    next_test_id = (int(max_test_id) + 1) if max_test_id is not None else 1

    test_id = None  # Initialize test_id as None

    if request.method == 'POST':
        form = HaematologyForm(request.POST)
        if form.is_valid():
            patient_id = form.cleaned_data['patient_id']
            try:
                # Fetch the PatientMaster instance using the patient_id
                patient = PatientMaster.objects.get(pk=patient_id)

                # Create a Haematology instance without saving it yet
                haematology_test = form.save(commit=False)
                haematology_test.test_id = next_test_id
                haematology_test.patient = patient

                # Populate the Haematology instance with data from PatientMaster
                haematology_test.patientname = patient.patientname
                haematology_test.age = patient.age
                haematology_test.gender = patient.gender
                haematology_test.mobile = patient.mobile
                haematology_test.email = patient.email

                # Save the Haematology instance
                haematology_test.save()

                # Get checkbox values for sending emails
                send_patient_email = request.POST.get('send_patient_email') == 'on'
                send_doctor_email = request.POST.get('send_doctor_email') == 'on'

                # Generate PDF Report as a BytesIO object
                pdf_buffer = BytesIO()
                generate_haematology_pdf(haematology_test, pdf_buffer)

                # Send email to patient if checked
                if send_patient_email:
                    email = EmailMessage(
                        'Haematology Test Result',
                        f'Dear {patient.patientname}, your haematology test (ID: {next_test_id}) has been added successfully. Please find the report attached.',
                        'your-email@example.com',  # Sender email
                        [patient.email]
                    )
                    email.attach(f'hae_{next_test_id}.pdf', pdf_buffer.getvalue(), 'application/pdf')
                    email.send()
                    messages.success(request, 'Email sent to the patient.')

                # Reset the buffer for the next email
                pdf_buffer.seek(0)

                # Send email to doctor if checked
                if send_doctor_email and patient.refbydoctor:
                    email = EmailMessage(
                        'Haematology Test Notification',
                        f'Dear {patient.refbydoctor.doctorname}, a new haematology test for patient {patient.patientname} (ID: {next_test_id}) has been recorded. Please find the report attached.',
                        'your-email@example.com',  # Sender email
                        [patient.refbydoctor.email]
                    )
                    email.attach(f'haematology_report_{next_test_id}.pdf', pdf_buffer.getvalue(), 'application/pdf')
                    email.send()
                    messages.success(request, 'Email sent to the doctor.')

                test_id = haematology_test.test_id  # Set test_id to the saved haematology test's ID

                messages.success(request, 'Haematology test added successfully.')
                form = HaematologyForm(initial={'test_id': next_test_id})
                return render(request, 'addhaematology.html', {'form': form, 'next_test_id': next_test_id, 'test_id': test_id})
            except PatientMaster.DoesNotExist:
                messages.error(request, 'Patient ID not found.')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')

    # If it's a GET request, show the form with initial test_id
    form = HaematologyForm(initial={'test_id': next_test_id})
    return render(request, 'addhaematology.html', {'form': form, 'next_test_id': next_test_id, 'test_id': test_id})


# Utility function to generate the PDF
def generate_haematology_pdf(haematology_test, buffer):
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Add title
    title = Paragraph("Sur Pathology Station Road Durg", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Add a horizontal line
    elements.append(Paragraph("<hr/>", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Add patient details
    patient_info = [
        ["Patient Name:", haematology_test.patient.patientname],
        ["Patient Age:", str(haematology_test.age)],
        ["Patient Gender:", haematology_test.gender],
        ["Patient Mobile:", haematology_test.mobile],
        ["Patient Email:", haematology_test.email],
    ]
    patient_table = Table(patient_info)
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(patient_table)
    elements.append(Spacer(1, 12))

    # Add report title
    report_title = Paragraph("Haematology Test Report", styles['Title'])
    elements.append(report_title)
    elements.append(Spacer(1, 12))

    # Add test details
    test_info = [
        ["Test ID:", str(haematology_test.test_id)],
        ["Test Date:", str(haematology_test.test_date)],
        ["Haemoglobin:", str(haematology_test.haemoglobin)],
        ["RBC Count:", str(haematology_test.rbc_count)],
        ["Platelets:", str(haematology_test.platelets)],
        ["PCV:", str(haematology_test.pcv)],
        ["MCV:", str(haematology_test.mcv)],
        ["MCH:", str(haematology_test.mch)],
        ["MCHC:", str(haematology_test.mchc)],
        ["Reticulocyte Count:", str(haematology_test.reticulocyte_count)],
        ["Bleeding Time:", str(haematology_test.bleeding_time)],
        ["Clotting Time:", str(haematology_test.clotting_time)],
        ["Eosinophil Exam:", str(haematology_test.eosinophil_exam)],
        ["Sickling Exam:", haematology_test.sickling_exam],
        ["Other Test:", haematology_test.other_test],
        ["Result:", haematology_test.result],
        ["Normal Value:", haematology_test.normal_value],
        ["Remarks:", haematology_test.remarks],
    ]
    test_table = Table(test_info)
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(test_table) 
    elements.append(Spacer(1, 12))

    # Add signature
    elements.append(Paragraph("Signature:", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Build the PDF into the buffer
    pdf.build(elements)


def viewhaematology(request):
    # Fetch all Haematology tests from the database
    haematology_tests = Haematology.objects.all()

    # Pass the test data to the template for rendering
    return render(request, 'viewhaematology.html', {
        'haematology_tests': haematology_tests
    })

def updatehaematology(request, test_id):
    # Fetch the Haematology test instance or show a 404 page if not found
    haematology_test = get_object_or_404(Haematology, test_id=test_id)

    if request.method == 'POST':
        # Bind form to POST data
        form = HaematologyForm(request.POST, instance=haematology_test)
        if form.is_valid():
            # Save the updated test if the form is valid
            form.save()
            messages.success(request, 'Data Updated Successfully.')
            return redirect('viewhaematology')
        else:
            # Add form errors to the context for debugging
            messages.error(request, 'Please correct the errors below.')
            print("Form Errors:", form.errors)  # Debugging information
    else:
        # Pre-populate the form with existing instance data
        form = HaematologyForm(instance=haematology_test)

    # Fetch the patient information from the PatientMaster associated with the Haematology test
    patient_data = haematology_test.patient  # Get the associated PatientMaster instance

    # Pre-fill the form with the patient's ID (as this can be changed)
    form.fields['patient_id'].initial = patient_data.patientid  # Assign initial patient ID value
    
    # Fetch additional data (refbydoctor and doctor_email) from PatientMaster
    patient_data.refbydoctor = patient_data.refbydoctor  # Fetch referred doctor name
    patient_data.email = patient_data.email  # Fetch doctor email

    # Render the update form template with the form and patient data
    return render(request, 'updatehaematology.html', {
        'form': form,
        'test_id': test_id,
        'patient_data': patient_data  # Pass the patient data to the template
    })


def deletehaematology(request, test_id):
    # Get the Haematology test record to be deleted
    haematology_test = get_object_or_404(Haematology, test_id=test_id)
    
    # Delete the record
    haematology_test.delete()
    
    # Add a success message
    messages.success(request, 'Haematology test deleted successfully.')
    
    # Redirect to the view page
    return redirect('viewhaematology')




def get_patient_data(request):
    patient_id = request.GET.get('patient_id')
    if patient_id:
        try:
            # Fetch the patient record
            patient = PatientMaster.objects.get(pk=patient_id)
            
            # Fetch the referring doctor's email (if any)
            doctor_email = patient.refbydoctor.email if patient.refbydoctor else None
            
            # Prepare the response data
            data = {
                'patientname': patient.patientname,
                'age': patient.age,
                'gender': patient.gender,
                'mobile': patient.mobile,
                'email': patient.email,  # Patient's email
                'doctorname': patient.refbydoctor.doctorname if patient.refbydoctor else None,
                'doctoremail': doctor_email,  # Referring doctor's email
            }
            return JsonResponse(data)
        except PatientMaster.DoesNotExist:
            return JsonResponse({'error': 'Patient not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def generate_haematology_report(request, test_id):
    # Fetch the haematology record using the test_id
    try:
        haematology_test = Haematology.objects.get(test_id=test_id)
    except Haematology.DoesNotExist:
        return HttpResponse("Haematology test not found.", content_type='text/plain')

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="haematology_report_{test_id}.pdf"'

    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Add title
    title = Paragraph("Sur Pathology Station Road Durg", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Add a horizontal line
    elements.append(Paragraph("<hr/>", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Add patient details
    patient_info = [
        ["Patient Name:", haematology_test.patient.patientname],
        ["Patient Age:", str(haematology_test.age)],
        ["Patient Gender:", haematology_test.gender],
        ["Patient Mobile:", haematology_test.mobile],
        ["Patient Email:", haematology_test.email],
    ]
    patient_table = Table(patient_info)
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(patient_table)
    elements.append(Spacer(1, 12))

    # Add a horizontal line
    elements.append(Paragraph("<hr/>", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Add report title
    report_title = Paragraph("Haematology Test Report", styles['Title'])
    elements.append(report_title)
    elements.append(Spacer(1, 12))

    # Add test details
    test_info = [
        ["Test ID:", str(haematology_test.test_id)],
        ["Test Date:", str(haematology_test.test_date)],
        ["Haemoglobin:", str(haematology_test.haemoglobin)],
        ["RBC Count:", str(haematology_test.rbc_count)],
        ["Platelets:", str(haematology_test.platelets)],
        ["PCV:", str(haematology_test.pcv)],
        ["MCV:", str(haematology_test.mcv)],
        ["MCH:", str(haematology_test.mch)],
        ["MCHC:", str(haematology_test.mchc)],
        ["Reticulocyte Count:", str(haematology_test.reticulocyte_count)],
        ["Bleeding Time:", str(haematology_test.bleeding_time)],
        ["Clotting Time:", str(haematology_test.clotting_time)],
        ["Eosinophil Exam:", str(haematology_test.eosinophil_exam)],
        ["Sickling Exam:", haematology_test.sickling_exam],
        ["Other Test:", haematology_test.other_test],
        ["Result:", haematology_test.result],
        ["Normal Value:", haematology_test.normal_value],
        ["Remarks:", haematology_test.remarks],
    ]
    test_table = Table(test_info)
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(test_table)
    elements.append(Spacer(1, 12))

    # Add a horizontal line
    elements.append(Paragraph("<hr/>", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Add signature
    elements.append(Paragraph("Signature:", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Build the PDF
    pdf.build(elements)

    return response




        
        

def test1(request):
    return render(request,'test1.html')

def test2(request):
    return render(request,'test2.html')

def test3(request):
    return render(request,'test3.html')

  
def handle_test1_submission(request):
    if request.method == 'POST' and 'submit_button1' in request.POST:
        # Process the form data for Form 1
        # ...
        return render(request,'addpatient.html') 
    else:
        return render(request, 'test1.html')  # Render the test1 page

def handle_test2_submission(request):
    if request.method == 'POST' and 'submit_button2' in request.POST:
        # Process the form data for Form 2
        return render(request,'test3.html') 
    else:
        return render(request, 'test2.html')  # Render the test1 page
  
     
def handle_test3_submission(request):
    if request.method == 'POST' and 'submit_button3' in request.POST:
        # Process the form data for Form 1
        # ...
        return render(request,'addpatient.html') 
    else:
        return render(request, 'about.html')  # Render the test1 page






   

#AAAA

def send_pdf_via_email(request):
    # Generate and save the PDF
    #pdf_filename = generate_pdf()
    
    
    pdf_filename1 = 'C:/Users/prade/Downloads/urine.pdf'

    # Prepare email details
    subject = 'Urine PDF Report'
    message = 'Please find the attached PDF report.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['pradeeplakhotia63@gmail.com']

    # Create EmailMessage instance
    email = EmailMessage(subject, message, email_from, recipient_list)

    # Attach the PDF
    with open(pdf_filename1, 'rb') as f:
        email.attach(pdf_filename1, f.read(), 'application/pdf')
        

    # Send the email
    email.send()

    return HttpResponse("Email with PDF sent successfully.")

#Report


def addbloodsugar(request):
    
    return render(request, 'addbloodsugar.html', {'bloodsugar_tests': addbloodsugar})