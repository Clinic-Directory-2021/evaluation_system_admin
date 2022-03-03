import statistics
from django.http.response import HttpResponse
import firebase_admin
from django.shortcuts import render,redirect
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
from numpy import double
import pyrebase
from datetime import datetime
import calendar
import xlwt
import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from main_app import functions as func

import json

config={
    "apiKey": "AIzaSyCRm30U4IA0BFi85g_5qfjF8QB4hF_iuqU",
    "authDomain": "evaluation-system-690d2.firebaseapp.com",
    "projectId": "evaluation-system-690d2",
    "databaseURL":"https://evaluation-system-690d2-default-rtdb.firebaseio.com/",
    "storageBucket": "evaluation-system-690d2.appspot.com",
    "messagingSenderId": "69328407149",
    "appId": "1:69328407149:web:c7b6326bf6d40a67140d64",
    "measurementId": "G-687GYC9DLD"
}
#`Initialising database, auth and firebase for further use
cred = credentials.Certificate("main_app/ServiceAccountKey.json")
firebase=pyrebase.initialize_app(config)
firebase_admin.initialize_app(cred)
authe = firebase.auth()
database=firebase.database()
db = firestore.client()


# Create your views here.
# def login_error(request):
#     return render(request,'file_403_header.html')
# def home_error(request):
#     return render(request,'file_403_home.html')
def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def dashboard(request):
        evaluation_report = db.collection(u'evaluation_report').get()
        seminar_report = db.collection(u'seminar_report').get()
        evaluator_report = db.collection(u'evaluator_report').get()
        # facilitator_report = db.collection(u'facilitator_report').get()
        evaluation_counter = 0
        seminar_counter = 0
        evaluator_counter = 0
        facilitator_counter = 0
        for doc in evaluation_report:
            evaluation_counter = evaluation_counter + 1
        for doc in seminar_report:
            seminar_counter = seminar_counter + 1
        for doc in evaluator_report:
            evaluator_counter = evaluator_counter + 1
        # for doc in facilitator_report:
        #     facilitator_counter = facilitator_counter + 1
        
        open_seminar = db.collection(u'seminars').get()
        pass_data = {
            "evaluation_counter":evaluation_counter,
            "seminar_counter":seminar_counter,
            "evaluator_counter":evaluator_counter,
            "seminar_data":[seminar.to_dict() for seminar in open_seminar]
            # "facilitator_counter":facilitator_counter
        }
        
        return render(request,'dashboard.html', pass_data)

def dashboard_post(request):
      # request should be ajax and method should be POST.
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    open_seminar = db.collection(u'seminars').get()
    if is_ajax and request.method == "POST":
        return JsonResponse({"instance": [seminar.to_dict() for seminar in open_seminar]}, status=200)
    return JsonResponse({'status': 'Invalid request'}, status=400)

def manage_seminar(request):
    try:
        docs = db.collection(u'seminars').get()
        seminar_id = {
            
        }
        ctr = 0
        for doc in docs:
            ctr = ctr + 1
            seminar_id[ctr] = doc.id 
            return render(request,'manage_seminar.html',{"seminar_data":[doc.to_dict() for doc in docs]})
    except:
        return render(request,'manage_seminar.html')
    return render(request,'manage_seminar.html')

def manage_facilitator(request):
    docs = db.collection(u'facilitators').get()
    facilitator_id = {
        
    }
    ctr = 0
    for doc in docs:
        ctr = ctr + 1
        facilitator_id[ctr] = doc.id 
        return render(request,'manage_facilitator.html',{"facilitator_data":[doc.to_dict() for doc in docs],"facilitator_id":id})
    return render(request,'manage_facilitator.html')

def manage_evaluator(request):
    try:
        evaluators = db.collection(u'evaluators').get()
        return render(request,'manage_evaluator.html',{"evaluator_data":[doc.to_dict() for doc in evaluators]})
    except:
        return render(request, 'manage_evaluator.html')

    
    

def report(request):
    try:
        evaluation_report = db.collection(u'evaluation_report').get()
        seminar_report = db.collection(u'seminar_report').get()
        evaluator_report = db.collection(u'evaluator_report').get()
        # facilitator_report = db.collection(u'facilitator_report').get()
        evaluation_counter = 0
        seminar_counter = 0
        evaluator_counter = 0
        facilitator_counter = 0
        for doc in evaluation_report:
            evaluation_counter = evaluation_counter + 1
        for doc in seminar_report:
            seminar_counter = seminar_counter + 1
        for doc in evaluator_report:
            evaluator_counter = evaluator_counter + 1
        # for doc in facilitator_report:
        #     facilitator_counter = facilitator_counter + 1
        
        pass_data = {
            "evaluation_counter":evaluation_counter,
            "seminar_counter":seminar_counter,
            "evaluator_counter":evaluator_counter,
            # "facilitator_counter":facilitator_counter
            }
        return render(request, 'report.html',pass_data)
    except Exception as e:
        return render(request, 'report.html')

def logout(request):
    try:
        del request.session['user_id']
    except:
        return redirect('/')
    return redirect('/')

def forgot_password(request):
    return render(request, 'forgot_password.html')

def add_seminar(request):
    facilitators = db.collection(u'facilitators').get()
    for facilitator_data in facilitators:
        return render(request,'add_seminar.html',{"facilitators":[facilitator_data.to_dict()]})
    return render(request, 'add_seminar.html')


def add_facilitator(request):
    return render(request, 'add_facilitator.html')

def add_evaluator(request):
    return render(request, 'add_evaluator.html')
    
def view_seminar_information(request):
    try:
        #* This will be need in the future to fetch current id of the seminar
        current_id = request.GET.get('current_id')
        evaluators = db.collection(u'evaluators').get()
        evaluator_count = 0;

        #Evaluator count
        for doc in evaluators:
            evaluator_count = evaluator_count + 1

        #Evaluation data
        evaluations = db.collection(u'evaluations').document(str(current_id))
        seminar = evaluations.get()
        seminar_title = u'{}'.format(seminar.to_dict()['seminar_title'])
        # seminar_date_id = str(u'{}'.format(seminar.to_dict()['seminar_date_id']))
        seminar_id = u'{}'.format(seminar.to_dict()['seminar_id'])
        date = u'{}'.format(seminar.to_dict()['date'])
        program_owner = u'{}'.format(seminar.to_dict()['program_owner'])
        program_owner_position = u'{}'.format(seminar.to_dict()['program_owner_position'])
        evaluation_data = evaluations.collection('evaluators').get()
        evaluation_count = 0
        evaluator_id = ""
        for doc in evaluation_data:
            evaluator_id = str(doc.id)
            print(evaluator_id)
            if doc.exists:
                evaluation_count += 1
            else:
                print(u'No such document!')
        pass_data = {
            "seminar_title":str(seminar_title),
            "seminar_id":str(seminar_id),
            "evaluation_data":[doc.to_dict() for doc in evaluation_data],
            "evaluation_count":str(evaluation_count),
            "evaluator_id":str(evaluator_id),
            "evaluator_count":str(evaluator_count),
            "date":str(date),
            "program_owner":str(program_owner),
            "program_owner_position":str(program_owner_position)}
            
        return render(request, 'view_seminar_information.html',pass_data)
        
    except Exception as e:
        print('Your error is: ' + str(e))
    return render(request, 'view_seminar_information.html')

def edit_seminar(request):
    current_id = request.GET.get('current_id')
    request.session['current_id'] =  current_id
    seminars = db.collection(u'seminars').document(current_id)
    seminar = seminars.get()

    seminar_title = u'{}'.format(seminar.to_dict()['seminar_title'])
    program_owner = u'{}'.format(seminar.to_dict()['program_owner'])
    seminar_start= u'{}'.format(seminar.to_dict()['seminar_start'])
    seminar_end = u'{}'.format(seminar.to_dict()['seminar_end'])
    program_owner_position = u'{}'.format(seminar.to_dict()['program_owner_position'])
    seminar_description = u'{}'.format(seminar.to_dict()['seminar_description'])
    status = u'{}'.format(seminar.to_dict()['status'])
    
    
    facilitators = seminars.collection(u'facilitators').get()
    for id in facilitators:
        print(str(id.id))
    pass_data = {
        "seminar_title":seminar_title,
        "program_owner":program_owner,
        "program_owner_position":program_owner_position,
        "seminar_start":seminar_start,
        "seminar_end":seminar_end,
        "seminar_description":seminar_description,
        "status":status,
        "facilitator":[facilitator_data.to_dict() for facilitator_data in facilitators],
    }
    return render(request,'edit_seminar.html',pass_data)
    
def edit_facilitator(request):
    current_id = request.GET.get('current_id')
    request.session['current_id'] =  current_id
    doc_ref = db.collection(u'facilitators').document(current_id)
    doc = doc_ref.get()
    facilitator_name = u'{}'.format(doc.to_dict()['facilitator_name'])
    department = u'{}'.format(doc.to_dict()['department'])
    rate = u'{}'.format(doc.to_dict()['rate'])
    return render(request,'edit_facilitator.html',{"facilitator_name":facilitator_name,"department":department,"rate":rate})

def edit_evaluator(request):
    try:
        current_id = str(request.GET.get('current_id'))
        request.session['current_id'] =  current_id
        doc_ref = db.collection(u'evaluators').document(current_id)
        doc = doc_ref.get()
        if doc.exists:
            first_name = u'{}'.format(doc.to_dict()['first_name'])
            middle_name = u'{}'.format(doc.to_dict()['middle_name'])
            last_name = u'{}'.format(doc.to_dict()['last_name'])
            email= u'{}'.format(doc.to_dict()['email'])
            gender = u'{}'.format(doc.to_dict()['gender'])
            school = u'{}'.format(doc.to_dict()['school_office'])
            phone_number = u'{}'.format(doc.to_dict()['phone_number'])
            position = u'{}'.format(doc.to_dict()['position'])
            uid = u'{}'.format(doc.to_dict()['uid'])
            date_created = u'{}'.format(doc.to_dict()['date_created'])
            pass_data = {
                "first_name":first_name,
                "middle_name":middle_name,
                "last_name":last_name,
                "email":email,
                "gender":gender,
                "school":school,
                "phone_number":phone_number,
                "position":position,
                "uid":uid,
                "evaluator_id":current_id,
                "date_created":date_created
                }
            print(phone_number)
            return render(request,'edit_evaluator.html',pass_data)
        else:
            print('ssss')
        return render(request,'edit_evaluator.html')
    except Exception as e:
        print(str(e))
        validation_text = str(e)
        return render(request,"manage_evaluator.html",{"validation_text":validation_text})

def total_evaluations(request):
    try:
        docs = db.collection(u'evaluation_report').get()
        evaluation_id = {
            
        }
        ctr = 0
        for doc in docs:
            ctr = ctr + 1
            evaluation_id[ctr] = doc.id 
            return render(request,'total_evaluations.html',{"evaluation_data":[doc.to_dict() for doc in docs],"evaluation_id":id})
    except Exception as e:
        print('Your Error is: ' + str(e))
        return render(request,'total_evaluations.html')
    return render(request,'total_evaluations.html')

def total_seminars(request):
    docs = db.collection(u'seminar_report').get()
    seminar_id = {
        
    }
    ctr = 0
    for doc in docs:
        ctr = ctr + 1
        seminar_id[ctr] = doc.id 
        return render(request,'total_seminars.html',{"seminar_data":[doc.to_dict() for doc in docs]})
    return render(request,'total_seminars.html')

def total_evaluators(request):
    try:
        docs = db.collection(u'evaluator_report').get()
        evaluator_id = {
            
        }
        ctr = 0
        for doc in docs:
            ctr = ctr + 1
            evaluator_id[ctr] = doc.id 
            return render(request,'total_evaluators.html',{"evaluator_data":[doc.to_dict() for doc in docs],"evaluator_id":id})
    except Exception as e:
        print('Your error is: ' + str(e))
        return render(request,'total_evaluators.html')
    return render(request,'total_evaluators.html')

def total_facilitators(request):
    docs = db.collection(u'facilitator_report').get()
    facilitator_id = {
        
    }
    ctr = 0
    for doc in docs:
        ctr = ctr + 1
        facilitator_id[ctr] = doc.id 
        return render(request,'total_facilitators.html',{"facilitator_data":[doc.to_dict() for doc in docs],"facilitator_id":id})
    return render(request,'total_facilitators.html')

def report_view_evaluation_info(request):
    try:
        #* This will be need in the future to fetch current id of the seminar
        current_id = request.GET.get('current_id')
        request.session['current_id'] = current_id
        print(current_id)
        
        #Evaluation report data
        evaluations = db.collection(u'evaluation_report').document(str(current_id))
        seminar = evaluations.get()
        seminar_title = u'{}'.format(seminar.to_dict()['seminar_title'])
        seminar_id = u'{}'.format(seminar.to_dict()['seminar_id'])
        program_owner = u'{}'.format(seminar.to_dict()['program_owner'])
        date = u'{}'.format(seminar.to_dict()['date'])


        evaluation_data = evaluations.collection(u'evaluators').get()
        for doc in evaluation_data:
            print(f'{doc.id} => {doc.to_dict()}')
            evaluator_id = str(doc.id)
            evaluation_count = 0
            if doc.exists:
                evaluation_count = evaluation_count + 1
                pass_data = {
                    "seminar_title":seminar_title,
                    "seminar_id":seminar_id,
                    "evaluation_data":[doc.to_dict() for doc in evaluation_data],
                    "evaluation_count":evaluation_count,
                    "evaluator_id":evaluator_id,
                    'program_owner':program_owner,
                    "date":date}
                return render(request, 'report_view_evaluation_info.html',pass_data)
        else:
            print(u'No such document!')
    except:
        print('ssss')
    return render(request,'report_view_evaluation_info.html')
    
def report_view_evaluator(request):
    current_id = str(request.GET.get('current_id'))
    request.session['current_id'] =  current_id
    doc_ref = db.collection(u'evaluator_report').document(current_id)
    doc = doc_ref.get()
    if doc.exists:
        first_name = u'{}'.format(doc.to_dict()['first_name'])
        middle_name = u'{}'.format(doc.to_dict()['middle_name'])
        last_name = u'{}'.format(doc.to_dict()['last_name'])
        email= u'{}'.format(doc.to_dict()['email'])
        gender = u'{}'.format(doc.to_dict()['gender'])
        school = u'{}'.format(doc.to_dict()['school_office'])
        phone_number = u'{}'.format(doc.to_dict()['phone_number'])
        position = u'{}'.format(doc.to_dict()['position'])

        return render(request,'report_view_evaluator.html',{"first_name":first_name,"middle_name":middle_name,"last_name":last_name,"email":email,"gender":gender,"school":school,"phone_number":phone_number,"position":position})
    else:
        print('ssss')
    return render(request,'report_view_evaluator.html')
#post backends
def postsignIn(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    validation_text = "";
    if email == "" or password == "":
        validation_text = "Please input all required fields."
        return render(request, "login.html",{"validation_text":validation_text})
    else:
        if email == 'DepedMalolos':
            if password == 'DepedMalolos':
                evaluation_report = db.collection(u'evaluation_report').get()
                seminar_report = db.collection(u'seminar_report').get()
                evaluator_report = db.collection(u'evaluator_report').get()
                # facilitator_report = db.collection(u'facilitator_report').get()
                evaluation_counter = 0
                seminar_counter = 0
                evaluator_counter = 0
                facilitator_counter = 0
                for doc in evaluation_report:
                    evaluation_counter = evaluation_counter + 1
                for doc in seminar_report:
                    seminar_counter = seminar_counter + 1
                for doc in evaluator_report:
                    evaluator_counter = evaluator_counter + 1
                # for doc in facilitator_report:
                #     facilitator_counter = facilitator_counter + 1
                
                open_seminar = db.collection(u'seminars').get()
                pass_data = {
                    "evaluation_counter":evaluation_counter,
                    "seminar_counter":seminar_counter,
                    "evaluator_counter":evaluator_counter,
                    "seminar_data":[seminar.to_dict() for seminar in open_seminar]
                    # "facilitator_counter":facilitator_counter
                }
                return render(request,'dashboard.html', pass_data)
        else:        
            return render(request, "login.html")

def postsignUp(request):
     first_name = request.POST.get('first_name')
     last_name = request.POST.get('last_name')
     email = request.POST.get('email')
     password = request.POST.get('password')
     confirm_password = request.POST.get('confirm_password')
     try:
        # creating a user with the given email and password
        if password == confirm_password:
            user=authe.create_user_with_email_and_password(email,password)
            uid = user['localId']
            data = {
                u'admin_id':uid,
                u'first_name': first_name,
                u'last_name': last_name,
            }
            db.collection(u'admins').document(uid).set(data)
            idtoken = request.session['uid']
        else:
             return render(request,"register.html",{"register_message":"Password and Confirm Password is not match"})
     except:   
        return render(request, "register.html")
     message = "Successfully Registered."
     return render(request,"login.html",{"register_message":message})

def forgot_password_func(request):
    forgot_pass_email = request.POST.get('forgot_pass_email')
    try:
        authe.send_password_reset_email(forgot_pass_email)
        return render(request,'login.html',{"forgot_password_message":"Successfully sent request to change password. Please check your email."})
    except:
        return render(request,'forgot_password.html',{"forgot_password_message","Email not found."})

def post_add_seminar(request):
    seminar_title = request.POST.get('seminar_title')
    seminar_start = request.POST.get('seminar_start')
    seminar_end = request.POST.get('seminar_end')
    program_owner = request.POST.get('program_owner')
    program_owner_position = request.POST.get('program_owner_position')
    seminar_description = request.POST.get('seminar_description')
    facilitator_list = str(request.POST.get('facilitator_list'))
    validation = request.POST.get('validation')
    date_created = datetime.now()
    seminar_id =  calendar.timegm(date_created.timetuple())
    facilitator_id = calendar.timegm(date_created.timetuple())
    try:
        if validation == "yes":
                data = {
                        u'seminar_title': seminar_title,
                        u'seminar_start': str(seminar_start),
                        u'seminar_end': str(seminar_end),
                        u'program_owner': program_owner,
                        u'program_owner_position':program_owner_position,
                        u'seminar_description': seminar_description,
                        u'date_created': str(date_created.strftime('%Y-%m-%d')),
                        u'status':"close",
                        u'seminar_id':str(seminar_id),
                        u'ongoing':"false"
                    }
                seminar = db.collection(u'seminars').document(str(seminar_id))
                seminar.set(data)
                seminar_report = db.collection(u'seminar_report').document(str(seminar_id))
                seminar_report.set(data)
                to_list = facilitator_list.split(';')
                for data in to_list:
                    if data == '':
                        break
                    else:
                        to_list_2 = data.split('=')
                        facilitator_name = to_list_2[0]
                        position = to_list_2[1]
                        facilitator_topic = to_list_2[2]
                        facilitator_time = to_list_2[3]
                        time = facilitator_time.split('-')
                    facilitator_data = {
                        "facilitator_id":facilitator_name,
                        "position":position,
                        "facilitator_name":facilitator_name,
                        "topic":facilitator_topic,
                        "start_time":time[0],
                        "end_time":time[1]
                    }
                    seminar.collection('facilitators').document(facilitator_name).set(facilitator_data)
                    seminar_report.collection('facilitators').document(facilitator_name).set(facilitator_data)
                
                #to traverse manage seminar
                docs = db.collection(u'seminars').get()
                seminar_id = {
                    
                }
                ctr = 0
                for doc in docs:
                    ctr = ctr + 1
                    seminar_id[ctr] = doc.id 
                    return render(request,'manage_seminar.html',{"seminar_data":[doc.to_dict() for doc in docs]})
                return render(request,'manage_seminar.html')
        else:
            return render(request,'add_seminar.html',{"validation":"hello"})
    except Exception as e:
                print('You error is: ' + str(e))
                return render(request,'add_seminar.html')

def post_add_facilitator(request):
        full_name = request.POST.get('facilitator_first_name') + " " + request.POST.get('facilitator_last_name')
        department = request.POST.get('department')
        date_created = datetime.now()
        facilitator_id =  calendar.timegm(date_created.timetuple())
        try:
            data = {
            u'facilitator_name': full_name,
            u'department': department,
            u'date_created': str(date_created),
            u'rate':"0",
            u'facilitator_id':facilitator_id,
            }
            db.collection(u'facilitators').document(str(facilitator_id)).set(data)
            db.collection(u'facilitator_report').document(str(facilitator_id)).set(data)
        except:
            return render(request,'add_facilitator.html')
        docs = db.collection(u'facilitators').get()
        facilitator_id = {
            
        }
        ctr = 0
        for doc in docs:
            ctr = ctr + 1
            facilitator_id[ctr] = doc.id 
            return render(request,'manage_facilitator.html',{"facilitator_data":[doc.to_dict() for doc in docs],"facilitator_id":id})
        return render(request,'manage_facilitator.html')

def post_add_evaluator(request):
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        school = request.POST.get('school')
        position = request.POST.get('position')
        phone_number = request.POST.get('phone_number')
        email_split = email.split('@')
        password = "12345678"
        validation_text = ""
        if email_split[1] != "deped.gov.ph":
            validation_text = "Invalid email format.You should use deped.gov.ph i.e juan.delacruz@deped.gov.ph"
            return render(request,'add_evaluator.html',{"validation_text":validation_text})
        else:
            date_created = datetime.now()
            evaluator_id =  calendar.timegm(date_created.timetuple())
            if func.has_numbers(first_name) or func.has_numbers(middle_name) or func.has_numbers(last_name):
                try:
                    user=authe.create_user_with_email_and_password(email,password)
                    uid = user['localId']
                    data = {
                    u'evaluator_id':str(evaluator_id),
                    u'first_name': first_name ,
                    u'middle_name': middle_name,
                    u'last_name': last_name,
                    u'email':str(email),
                    u'gender': gender,
                    u'school_office': school,
                    u'phone_number': phone_number,
                    u'position':position,
                    u'date_created':date_created,
                    u'uid':uid,
                    u'password':password
                    }
                    db.collection(u'evaluators').document(str(evaluator_id)).set(data)
                    db.collection(u'evaluator_report').document(str(evaluator_id)).set(data)
                except Exception as e:
                    print(str(e))
                    print(email)
                    return render(request,'add_evaluator.html',{'validation_text':"Email Exist"})
                docs = db.collection(u'evaluators').get()
                evaluator_id = {
                    
                }
                ctr = 0
                for doc in docs:
                    ctr = ctr + 1
                    evaluator_id[ctr] = doc.id 
                    pass_data = {
                    "validation_text":"Successfully Add A Evaluator. His/Her Default password is 12345678",
                    "evaluator_data":[doc.to_dict() for doc in docs],
                    "evaluator_id":id}
                    return render(request,'manage_evaluator.html',pass_data)
            else:
                validation_text = "Invalid name format.Numbers and character is not allowed to use"
                return render(request,'add_evaluator.html',{"validation_text":validation_text})

def post_edit_seminar(request):
    # try:
        facilitator_list = str(request.POST.get('facilitator_list'))
        current_id = request.session['current_id']
        seminar_title = request.POST.get('seminar_title')
        seminar_start = request.POST.get('seminar_start')
        seminar_end = request.POST.get('seminar_end')
        program_owner = request.POST.get('program_owner')
        program_owner_position = request.POST.get('program_owner_position')
        seminar_description = request.POST.get('seminar_description')
        status = request.POST.get('status')
        update_seminar = db.collection(u'seminars').document(current_id)
        update_seminar_report = db.collection(u'seminar_report').document(current_id)
        updated_data = {
            u'seminar_title': seminar_title,
            u'seminar_start': seminar_start,
            u'seminar_end': seminar_end,
            u'program_owner': program_owner,
            u'program_owner_position': program_owner_position,
            u'seminar_description': seminar_description,
            u'status':status
            }
        update_seminar.update(updated_data)
        update_seminar_report.update(updated_data)

        to_list = facilitator_list.split(';')
        for data in to_list:
            if data == '':
              break
            else:
                to_list_2 = data.split('=')
                facilitator_name = to_list_2[0]
                position = to_list_2[1]
                topic = to_list_2[2]
                facilitator_time = to_list_2[3]
                time = facilitator_time.split('-')
                facilitator_data = {
                "facilitator_id":facilitator_name,
                "facilitator_name":facilitator_name,
                "position":position,
                "topic":topic,
                "start_time":time[0],
                "end_time":time[1]
                }
                update_seminar.collection('facilitators').document(facilitator_name).set(facilitator_data)
                update_seminar_report.collection('facilitators').document().set(facilitator_data)

        docs = db.collection(u'seminars').get()
        seminar_id = {
            
        }
        ctr = 0
        for doc in docs:
            ctr = ctr + 1
            seminar_id[ctr] = doc.id 
            return render(request,'manage_seminar.html',{"seminar_data":[doc.to_dict() for doc in docs]})
    # except:
    #       return render(request,'edit_seminar.html')

# def post_edit_facilitator(request):
#     current_id = request.session['current_id']
#     facilitator_name = request.POST.get('facilitator_name')
#     department = request.POST.get('department')
#     rate = request.POST.get('rate')
#     update_seminar = db.collection(u'facilitators').document(current_id)
#     updated_data = {
#         u'facilitator_name': facilitator_name,
#         u'department':department,
#         u'rate':rate
#         }
#     update_seminar.update(updated_data)


#     docs = db.collection(u'facilitators').get()
#     seminar_id = {
        
#     }
#     ctr = 0
#     for doc in docs:
#         ctr = ctr + 1
#         seminar_id[ctr] = doc.id 
#     return render(request,'manage_facilitator.html',{"facilitator_data":[doc.to_dict() for doc in docs]})

def post_edit_evaluator(request):
    current_id = request.session['current_id']
    first_name = request.POST.get('first_name')
    middle_name = request.POST.get('middle_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    gender = request.POST.get('gender')
    phone_number = request.POST.get('phone_number')
    school = request.POST.get('school')
    position = request.POST.get('position')
    uid = request.POST.get('uid')
    evaluator_id = request.POST.get('evaluator_id')
    date_created = request.POST.get('date_created')
    try:
        update_evaluator = db.collection(u'evaluators').document(current_id)
        updated_data = {
            u'first_name': first_name,
            u'middle_name':middle_name,
            u'last_name':last_name,
            u'email': str(email),
            u'gender':gender,
            u'phone_number':phone_number,
            u'school_office': school,
            u'position':position,
            u"uid":uid,
            u"evaluator_id":evaluator_id,
            u"date_created":date_created
            }
        update_evaluator.update(updated_data)

        docs = db.collection(u'evaluators').get()
        # evaluator_id = {
            
        # }
        ctr = 0
        for doc in docs:
            ctr = ctr + 1
            # evaluator_id[ctr] = doc.id 
            return render(request,'manage_evaluator.html',{"evaluator_data":[doc.to_dict() for doc in docs],"validation_text":"Successfully Edit " + first_name + " " + middle_name + " " + last_name + " Info."})
    except Exception as e:
        print(str(e))
        return render(request,'manage_evaluator.html')

def post_start_seminar(request):
    current_id = request.POST.get('seminar_id')
    seminar_document = db.collection(u'seminars').document(current_id)
    seminar_document.update({u'ongoing': "true"})
    seminar_document.update({u'status': "open"})
    docs = db.collection(u'seminars').get()
    seminar_docs =  seminar_document.get()
    seminar_name = u'{}'.format(seminar_docs.to_dict()['seminar_title'])
    program_owner_position = u'{}'.format(seminar_docs.to_dict()['program_owner_position'])
    program_owner = u'{}'.format(seminar_docs.to_dict()['program_owner'])
    date_created = datetime.now()
    seminar_date_id = calendar.timegm(date_created.timetuple())
    seminar_id = {
        
    }
    ctr = 0

    data = {
    u'date': date_created,
    u'seminar_date_id': seminar_date_id,
    u'seminar_id': current_id,
    u'seminar_title':seminar_name,
    u'program_owner':program_owner,
    u'program_owner_position':program_owner_position,
    u'status':"open"
    }
    print(seminar_date_id)
    evaluations_collection = db.collection(u'evaluations').document(current_id)
    evaluations_collection.set(data)
    for doc in docs:
        ctr = ctr + 1
        seminar_id[ctr] = doc.id 
        return render(request,'manage_seminar.html',{"seminar_data":[doc.to_dict() for doc in docs]})
    return render(request,'manage_seminar.html')

def post_view_seminar_actions(request):
    #POST VALUES      
    try:
            program_owner = request.POST.get('program_owner')
            program_owner_position = request.POST.get('program_owner_position')
            seminar_id = request.POST.get('seminar_id')
            evaluator_id = request.POST.get('evaluator_id')
            seminar_title = request.POST.get('seminar_title')
            date_created = request.POST.get('date')
            print(request.POST.get('date'))
            evaluation_report_field = {
                'date': date_created,
                "program_owner": program_owner,
                "program_owner_position": program_owner_position,
                "seminar_id":seminar_id,
                "seminar_title":seminar_title
            }

    #Evaluation Report collection creation
            evaluation_report = db.collection(u'evaluation_report').document(seminar_id) 
            evaluation_report.set(evaluation_report_field)
            evaluations = evaluation_report.collection('evaluators')

    #Evaluationlist traversion
            evaluations_list = db.collection(u'evaluations').document(seminar_id)
            evaluation_sub = evaluations_list.collection('evaluators')
            get_data = evaluation_sub.get()
            for doc in get_data:
                evaluations.document(doc.id).set(doc.to_dict())
                facilitator = evaluation_sub.document(doc.id).collection('facilitators')
                facilitator_report = evaluations.document(doc.id).collection('facilitators')
                get_facilitator = facilitator.get()
                for facilitator_data in get_facilitator:
                    facilitator_report.document(facilitator_data.id).set(facilitator_data.to_dict())
                    
    #Deleting seminar after closing
            # db.collection(u'seminars').document(seminar_id).collection('facilitators').delete()
            # db.collection(u'seminars').document(seminar_id).delete()
            update_seminar = db.collection(u'seminars').document(seminar_id)
            update_seminar.update({u'ongoing': "false"})
            update_seminar.update({u'status': u'close'})

    #Calling again the seminars in dashboard
            open_seminar = db.collection(u'seminars').get()
            return render(request,'dashboard.html', {"seminar_data":[seminar.to_dict() for seminar in open_seminar]})
    except Exception as e:
        print(str(e))
        #Deleting seminar after closing
        db.collection(u'seminars').document(seminar_id).delete()
            # update_seminar = db.collection(u'seminars').document(seminar_id)
            # update_seminar.update({u'ongoing': "false"})
            # update_seminar.update({u'status': u'close'})

    #Calling again the seminars in dashboard
        open_seminar = db.collection(u'seminars').get()
        return render(request,'dashboard.html', {"seminar_data":[seminar.to_dict() for seminar in open_seminar]})

def delete_seminar(request):
    try:
        current_id = request.GET.get('current_id')
        # db.collection(u'seminars').document(current_id).delete()
        seminar = db.collection(u'seminars')
        seminar_doc = seminar.get()

        facilitator = seminar.document(current_id).collection('facilitators').get()
        for doc2 in facilitator:
            seminar.document(current_id).collection('facilitators').document(doc2.id).delete()

        seminar.document(str(current_id)).delete()
        # seminar_document.update({u'status': "close"})
        docs = db.collection(u'seminars').get()
        return render(request,'manage_seminar.html',{"seminar_data":[doc.to_dict() for doc in docs]})
    except Exception as e:
        print(str(e))
        docs = db.collection(u'seminars').get()
        return render(request,'manage_seminar.html',{"seminar_data":[doc.to_dict() for doc in docs]})

def delete_facilitator(request):
    current_id = request.GET.get('current_id')
    db.collection(u'facilitators').document(current_id).delete()
    docs = db.collection(u'facilitators').get()
    facilitator_id = {
        
    }
    ctr = 0
    for doc in docs:
        ctr = ctr + 1
        facilitator_id[ctr] = doc.id 
        return render(request,'manage_facilitator.html',{"facilitator_data":[doc.to_dict() for doc in docs],"facilitator_id":id})
    return render(request,'manage_facilitator.html')

def delete_evaluator(request):
    try:
        current_id = request.GET.get('current_id')
        evaluator_document = db.collection(u'evaluators').document(current_id)
        data = evaluator_document.get()
        uid_token =  u'{}'.format(data.to_dict()['uid'])
        already_evaluated = evaluator_document.collection('already_evaluated').get()
        history = evaluator_document.collection('history').get()
        for evaluated_doc in already_evaluated:
            evaluator_document.collection('already_evaluated').document(evaluated_doc.id).delete()
        for history_doc in already_evaluated:
            facilitator_doc = evaluator_document.collection('history').document(history_doc.id).collection('facilitators').get()
            for doc in facilitator_doc:
                evaluator_document.collection('history').document(history_doc.id).collection('facilitators').document(doc.id).delete()
                evaluator_document.collection('history').document(history_doc.id).delete()
        evaluator_document.delete()
        auth.delete_user(uid_token)
        docs = db.collection(u'evaluators').get()
        evaluator_id = {
            
        }
        ctr = 0
        for doc in docs:
            ctr = ctr + 1
            evaluator_id[ctr] = doc.id 
            return render(request,'manage_evaluator.html',{"evaluator_data":[doc.to_dict() for doc in docs],"evaluator_id":id})
        return render(request,'manage_evaluator.html')
    except Exception as e:
        print(str(e) + "is your error")
        docs = db.collection(u'evaluators').get()
        evaluator_id = {
            
        }
        ctr = 0
        for doc in docs:
            ctr = ctr + 1
            evaluator_id[ctr] = doc.id 
            return render(request,'manage_evaluator.html',{"evaluator_data":[doc.to_dict() for doc in docs],"evaluator_id":id})

#*Special function/s
def export_evaluation(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Evaluations' + str(datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Responses')
    row_num = 0
    font_style = xlwt.XFStyle()
    columns = ['#',
               'Timestamp',
               'Email Address',
               'Name',
               'Program objectives were clearly presented',
               'Program objectives were attained',
               'Program content was appropriate to trainees roles and responsibility',
               'Content delivered was based on authoritative and reliable sources',
               'Sessions activities were effective in generating learning',
               'Adult learning methodologies were used',
               'Program followed a logical order/structure',
               'Contribution of all trainees was encouraged',
               'Training program was delivered as planned',
               'Training program was managed effectively',
               'Training program was well-structured',
               'Appropriate to trainees needs',
               'Adequate',
               'Given on time',
               'Members were present when needed',
               'Members were courteous',
               'Members were efficient',
               'Members were responsive to the needs of the trainees',
               'What is your most significant learning for the day?',
               'What will you do differently as a School Head/Teacher/Personnel given your learning?',
               'How can the session be improved, if at all?',
               'Comments/Suggestions for the improvement of program management/operations.']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    current_id = request.session['current_id']
    docs = db.collection(u'evaluation_report').document(str(current_id))
    evaluator = docs.collection('evaluators').get()
    counter = 0
    for doc in evaluator:
        if doc.to_dict()['status'] == "evaluated":
            rows = {
                str(0): counter + 1,
                str(1): u'{}'.format(doc.to_dict()['date_posted']),
                str(2): u'{}'.format(doc.to_dict()['evaluatorEmail']),
                str(3): u'{}'.format(doc.to_dict()['full_name']),
                str(4): u'{}'.format(doc.to_dict()['q1']),
                str(5): u'{}'.format(doc.to_dict()['q2']),
                str(6): u'{}'.format(doc.to_dict()['q3']),
                str(7): u'{}'.format(doc.to_dict()['q4']),
                str(8): u'{}'.format(doc.to_dict()['q5']),
                str(9): u'{}'.format(doc.to_dict()['q6']),
                str(10): u'{}'.format(doc.to_dict()['q7']),
                str(11): u'{}'.format(doc.to_dict()['q8']),
                str(12): u'{}'.format(doc.to_dict()['q18']),
                str(13): u'{}'.format(doc.to_dict()['q19']),
                str(14): u'{}'.format(doc.to_dict()['q20']),
                str(15): u'{}'.format(doc.to_dict()['q21']),
                str(16): u'{}'.format(doc.to_dict()['q22']),
                str(17): u'{}'.format(doc.to_dict()['q23']),
                str(18): u'{}'.format(doc.to_dict()['q24']),
                str(19): u'{}'.format(doc.to_dict()['q25']),
                str(20): u'{}'.format(doc.to_dict()['q26']),
                str(21): u'{}'.format(doc.to_dict()['q27']),
                str(22): u'{}'.format(doc.to_dict()['c1']),
                str(23): u'{}'.format(doc.to_dict()['c2']),
                str(24): u'{}'.format(doc.to_dict()['c3']),
                str(25): u'{}'.format(doc.to_dict()['c4']),
            }
            row_num += 1
            for col_num in range(len(rows)):
                ws.write(row_num, col_num+1, rows.get(str(col_num+1)))
    wb.save(response)
    return response
def view_seminar(request):
    try:
        current_id = request.GET.get('current_id')
        request.session['current_id'] =  current_id
        seminars = db.collection(u'seminar_report').document(current_id)
        seminar = seminars.get()    

        seminar_title = u'{}'.format(seminar.to_dict()['seminar_title'])
        program_owner = u'{}'.format(seminar.to_dict()['program_owner'])
        
        
        facilitators = seminars.collection(u'facilitators').get()
        pass_data = {
            "seminar_title":seminar_title,
            "program_owner":program_owner,
            "facilitator":[facilitator_data.to_dict() for facilitator_data in facilitators]
        }
        return render(request,'view_seminar.html',pass_data)
    except Exception as e:
        print('Your error is: ' + str(e))
        return render(request,'view_seminar.html')



def link_callback(uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path
#PDF GENERATEDS
# def generate_pdf(path,response_name):
    

def generate_evaluator(request):
    try:
        datetime_now = datetime.now()
        template_path = "pdf_generated/generate_evaluators.html"


        #Calling firestore data
        evaluator_report = db.collection(u'evaluator_report').get()
        context = {'evaluator_data': [evaluator_data.to_dict() for evaluator_data in evaluator_report]}

        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="'+"generate_evaluator"+"-"+str(datetime_now)+".pdf"
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
        # if error then show some funy view
        if pisa_status.err:
            print(html)
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    except Exception as e:
        print(str(e))

def generate_seminar(request):
    try:
        datetime_now = datetime.now()
        template_path = "pdf_generated/generate_seminars.html"


        #Calling firestore data
        evaluator_report = db.collection(u'seminar_report').get()
        context = {'seminar_data': [evaluator_data.to_dict() for evaluator_data in evaluator_report]}

        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="'+"generate_seminar"+"-"+str(datetime_now)+".pdf"
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
        # if error then show some funy view
        if pisa_status.err:
            #print(html)
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    except Exception as e:
        print(str(e))
        return render(request,'total_seminars.html')
        
def post_delete_facilitator(request):
    #Calling session variables
    facilitator_id = request.GET.get('facilitator_id')
    current_id = request.session['current_id']

    #Calling the parent collection named: seminar
    seminars = db.collection(u'seminars').document(current_id)

    #Delete the specific facilitator
    seminars.collection(u'facilitators').document(facilitator_id).delete()

    #Traversing the specific seminar details
    seminar = seminars.get()
    seminar_title = u'{}'.format(seminar.to_dict()['seminar_title'])
    program_owner = u'{}'.format(seminar.to_dict()['program_owner'])
    status = u'{}'.format(seminar.to_dict()['status'])
    
    
    facilitators = seminars.collection(u'facilitators').get()
    pass_data = {
        "seminar_title":seminar_title,
        "program_owner":program_owner,
        "status":status,
        "facilitator":[facilitator_data.to_dict() for facilitator_data in facilitators]
    }
    return render(request,'edit_seminar.html',pass_data)
 
def post_edit_facilitator(request):
    #Calling session variables
    facilitator_id = request.GET.get('facilitator_id')
    facilitator_name = request.GET.get('facilitator_name')
    position = request.GET.get('position')
    topic = request.GET.get('topic')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    current_id = request.session['current_id']
    try:
        #Calling the parent collection named: seminar
        seminars = db.collection('seminars').document(current_id)

        #Traversing the specific seminar details
        seminar = seminars.get()
        seminar_title = u'{}'.format(seminar.to_dict()['seminar_title'])
        program_owner = u'{}'.format(seminar.to_dict()['program_owner'])
        program_owner_position = u'{}'.format(seminar.to_dict()['program_owner_position'])
        status = u'{}'.format(seminar.to_dict()['status'])
        
        
        facilitators = seminars.collection('facilitators')

        #Update data in subcollection name: facilitator
        update_data = {
            "facilitator_id":facilitator_id,
            "facilitator_name":facilitator_name,
            "position":position,
            "topic":topic,
            "start_time":start_time,
            "end_time":end_time   
        }
        facilitators.document(facilitator_id).update(update_data)

        #Traverse Facilitators
        traverse_facilitator = facilitators.get()
        pass_data = {
            "seminar_title":seminar_title,
            "program_owner":program_owner,
            "program_owner_position":program_owner_position,
            "status":status,
            "facilitator":[facilitator_data.to_dict() for facilitator_data in traverse_facilitator]
        }
        return render(request,'edit_seminar.html',pass_data)
    except Exception as e:
        print(str(e))
        print(facilitator_id)
        docs = db.collection(u'seminars').get()
        seminar_id = {
            
        }
        ctr = 0
        for doc in docs:
            ctr = ctr + 1
            seminar_id[ctr] = doc.id 
            return render(request,'manage_seminar.html',{"seminar_data":[doc.to_dict() for doc in docs],"error":str(e),"e":facilitator_id})


def link_callback(uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path
def get_summary_data(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            q1_dict = {
                "1":0,
                "2":0,
                "3":0,
                "4":0,
            }
            q2_dict = {
                "1":0,
                "2":0,
                "3":0,
                "4":0,
            }
            q3_dict = {
                "1":0,
                "2":0,
                "3":0,
                "4":0,
            }
            q4_dict = {
                "1":0,
                "2":0,
                "3":0,
                "4":0,
            }
            q5_dict = {
                "1":0,
                "2":0,
                "3":0,
                "4":0,
            }
            q6_dict = {
                "1":0,
                "2":0,
                "3":0,
                "4":0,
            }
            q7_dict = {
                "1":0,
                "2":0,
                "3":0,
                "4":0,
            }
            q8_dict = {
                "1":0,
                "2":0,
                "3":0,
                "4":0,
            }
            q18_dict = {
                "1":0,
                "2":0,
                "3":0,
                "4":0,
            }
            q19_dict = {
                "1":0,
                "2":0,
                "3":0,
                "4":0,
            }
            q20_dict = {
                "1":0,
                "2":0,
                "3":0,
                "4":0,
            }
            q21_dict = {
                "1":0,
                "2":0,
                "3":0,
                "4":0,
            }
            q22_dict = {
                "1":0,
                "2":0,
                "3":0,
                "4":0,
            }
            q23_dict = {
                "1":0,
                "2":0,
                "3":0,
                "4":0,
            }
            q24_dict = {
                "1":0,
                "2":0,
                "3":0,
                "4":0,
            }
            q25_dict = {
                "1":0,
                "2":0,
                "3":0,
                "4":0,
            }
            q26_dict = {
                "1":0,
                "2":0,
                "3":0,
                "4":0,
            }
            q27_dict = {
                "1":0,
                "2":0,
                "3":0,
                "4":0,
            }
            facilitator_response ={

            }
            facilitator_mean ={

            }
            facilitator_topic = {

            }
            facilitator_question = {
                "q9":"Exhibited full grasp of the topic",
                "q10":"Was sensitive to the participants' mood",
                "q11":"Asked stimulating questions",
                "q12":"Processed questions and responses to deepen learning",
                "q13":"Maintained positive learning environment",
                "q14":"Expressed ideas clearly",
                "q15":"Used appropriate training aids",
                "q16":"Observed appropriate attire",
                "q17":"Was able to firm up attainment of objectives of the session",
            }
            current_id = str(request.POST.get('seminar_id'))
            total_of_participant = 0
            total_of_participant2 = 0
            evaluation_report = db.collection(u'evaluation_report').document(current_id)
            evaluation_data = evaluation_report.get()
            seminar_title = u'{}'.format(evaluation_data.to_dict()['seminar_title'])
            program_owner = u'{}'.format(evaluation_data.to_dict()['program_owner'])
            program_owner_position = u'{}'.format(evaluation_data.to_dict()['program_owner_position'])
            # expected_participant = u'{}'.format(evaluation_data.to_dict()['expected_participant'])
            date = u'{}'.format(evaluation_data.to_dict()['date'])
            evaluators = evaluation_report.collection('evaluators')
            evaluators_data = evaluators.where('status','==','evaluated').get()
            evaluators_data2 = evaluators.get()
            for evaluator_data in evaluators_data:
                hello = evaluator_data.id
                facilitators = evaluators.document(evaluator_data.id).collection('facilitators').where('q17','>','0').get()
                for facilitators_data in facilitators:
                    facilitator_topic[facilitators_data.id] = facilitators_data.to_dict()['topic']
                    facilitator_response[facilitators_data.id] = {
                    "q9":{"1":0,"2":0,"3":0,"4":0,"mean":0},
                    "q10":{"1":0,"2":0,"3":0,"4":0,"mean":0},
                    "q11":{"1":0,"2":0,"3":0,"4":0,"mean":0},
                    "q12":{"1":0,"2":0,"3":0,"4":0,"mean":0},
                    "q13":{"1":0,"2":0,"3":0,"4":0,"mean":0},
                    "q14":{"1":0,"2":0,"3":0,"4":0,"mean":0},
                    "q15":{"1":0,"2":0,"3":0,"4":0,"mean":0},
                    "q16":{"1":0,"2":0,"3":0,"4":0,"mean":0},
                    "q17":{"1":0,"2":0,"3":0,"4":0,"mean":0},
                    }
            
   
            for evaluator_data in evaluators_data:
                facilitators = evaluators.document(evaluator_data.id).collection('facilitators').get()
                for facilitators_data in facilitators:
                    temp_dict = facilitators_data.to_dict()
                    for key,data_dict in temp_dict.items():
                                func.get_facilitator_rate(facilitator_response,facilitators_data.id,data_dict,key)  
            for data in evaluators_data2: 
                total_of_participant2 += 1             
            for data in evaluators_data:   
                total_of_participant += 1
                print(u'{}'.format(data.id))
                q1 = u'{}'.format(data.to_dict()['q1'])
                q2 = u'{}'.format(data.to_dict()['q2'])
                q3 = u'{}'.format(data.to_dict()['q3'])
                q4 = u'{}'.format(data.to_dict()['q4'])
                q5 = u'{}'.format(data.to_dict()['q5'])
                q6 = u'{}'.format(data.to_dict()['q6'])
                q7 = u'{}'.format(data.to_dict()['q7'])
                q8 = u'{}'.format(data.to_dict()['q8'])
                q18 = u'{}'.format(data.to_dict()['q18'])
                q19 = u'{}'.format(data.to_dict()['q19'])
                q20 = u'{}'.format(data.to_dict()['q20'])
                q21 = u'{}'.format(data.to_dict()['q21'])
                q22 = u'{}'.format(data.to_dict()['q22'])
                q23 = u'{}'.format(data.to_dict()['q23'])
                q24 = u'{}'.format(data.to_dict()['q24'])
                q25 = u'{}'.format(data.to_dict()['q25'])
                q26 = u'{}'.format(data.to_dict()['q26'])
                q27 = u'{}'.format(data.to_dict()['q27'])
                
                func.question_dict(q1,q1_dict)
                func.question_dict(q2,q2_dict)
                func.question_dict(q3,q3_dict)
                func.question_dict(q4,q4_dict)
                func.question_dict(q5,q5_dict)
                func.question_dict(q6,q6_dict)
                func.question_dict(q7,q7_dict)
                func.question_dict(q8,q8_dict)
                func.question_dict(q18,q18_dict)
                func.question_dict(q19,q19_dict)
                func.question_dict(q20,q20_dict)
                func.question_dict(q21,q21_dict)
                func.question_dict(q22,q22_dict)
                func.question_dict(q23,q23_dict)
                func.question_dict(q24,q24_dict)
                func.question_dict(q25,q25_dict)
                func.question_dict(q26,q26_dict)
                func.question_dict(q27,q27_dict)
            
            func.get_facilitator_mean(facilitator_response,total_of_participant)     
            q1_mean = func.get_mean(q1_dict, total_of_participant)
            q2_mean = func.get_mean(q2_dict, total_of_participant)
            q3_mean = func.get_mean(q3_dict, total_of_participant)
            q4_mean = func.get_mean(q4_dict, total_of_participant)
            q5_mean = func.get_mean(q5_dict, total_of_participant)
            q6_mean = func.get_mean(q6_dict, total_of_participant)
            q7_mean = func.get_mean(q7_dict, total_of_participant)
            q8_mean = func.get_mean(q8_dict, total_of_participant)
            q18_mean = func.get_mean(q18_dict, total_of_participant)
            q19_mean = func.get_mean(q19_dict, total_of_participant)
            q20_mean = func.get_mean(q20_dict, total_of_participant)
            q21_mean = func.get_mean(q21_dict, total_of_participant)
            q22_mean = func.get_mean(q22_dict, total_of_participant)
            q23_mean = func.get_mean(q23_dict, total_of_participant)
            q24_mean = func.get_mean(q24_dict, total_of_participant)
            q25_mean = func.get_mean(q25_dict, total_of_participant)
            q26_mean = func.get_mean(q26_dict, total_of_participant)
            q27_mean = func.get_mean(q27_dict, total_of_participant)

            mean_1 =  statistics.mean([q1_mean,q2_mean,q3_mean,q4_mean,q5_mean,q6_mean,q7_mean,q8_mean])
            mean_2 =  statistics.mean([q18_mean,q19_mean,q20_mean])
            mean_3 =  statistics.mean([q21_mean,q22_mean,q23_mean])
            mean_4 =  statistics.mean([q24_mean,q25_mean,q26_mean,q26_mean])

            print(mean_1)
            overall_mean = round(statistics.mean([mean_1,mean_2,mean_3,mean_4]),1)
            func.facilitator_overall_mean(facilitator_mean,facilitator_response)
            print(overall_mean)
            template_path = 'pdf_generated/generate_summary.html'
            context = {
                'seminar_title':seminar_title,
                'date_posted':date,
                'program_owner':program_owner,
                'program_owner_position':program_owner_position,
                # 'participatant_rate':(int(total_of_participant) / int(expected_participant)) * 100,
                'q1':q1_dict,
                'q2':q2_dict,
                'q3':q3_dict,
                'q4':q4_dict,
                'q5':q5_dict,
                'q6':q6_dict,
                'q7':q7_dict,
                'q8':q8_dict,
                'q18':q18_dict,
                'q19':q19_dict,
                'q20':q20_dict,
                'q21':q21_dict,
                'q22':q22_dict,
                'q23':q23_dict,
                'q24':q24_dict,
                'q25':q25_dict,
                'q26':q26_dict,
                'q27':q27_dict,
                "q1_mean":"{:.2f}".format(q1_mean),
                "q2_mean":"{:.2f}".format(q2_mean),
                "q3_mean":"{:.2f}".format(q3_mean),
                "q4_mean":"{:.2f}".format(q4_mean),
                "q5_mean":"{:.2f}".format(q5_mean),
                "q6_mean":"{:.2f}".format(q6_mean),
                "q7_mean":"{:.2f}".format(q7_mean),
                "q8_mean":"{:.2f}".format(q8_mean),
                "q18_mean":"{:.2f}".format(q18_mean),
                "q19_mean":"{:.2f}".format(q19_mean),
                "q20_mean":"{:.2f}".format(q20_mean),
                "q21_mean":"{:.2f}".format(q21_mean),
                "q22_mean":"{:.2f}".format(q22_mean),
                "q23_mean":"{:.2f}".format(q23_mean),
                "q24_mean":"{:.2f}".format(q24_mean),
                "q25_mean":"{:.2f}".format(q25_mean),
                "q26_mean":"{:.2f}".format(q26_mean),
                "q27_mean":"{:.2f}".format(q27_mean),
                "total_of_participants":total_of_participant,
                "total_of_participants2":total_of_participant2,
                "facilitator_response":facilitator_response,
                "facilitator_mean":facilitator_mean,
                "facilitator_topic":facilitator_topic,
                "test":mean_1,
                "mean_1":round(mean_1,1),
                "mean_2":round(mean_2,1),
                "mean_3":round(mean_3,1),
                "mean_4":round(mean_4,1),
                "facilitator_question":facilitator_question,
                "overall_mean":overall_mean,
                "comments":[comment_data.to_dict() for comment_data in evaluators_data]
                }
            print('11111111111111111111111111')
            for key, val in facilitator_mean.items():
                print('key is ', key)
                print('val is ', val)
            print('11111111111111111111111111')
            return JsonResponse(context)
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')

def get_summary_data3(request):
            template_path = 'pdf_generated/generate_summary.html'
            context = {
            'seminar_title':request.session['seminar_title'],
            'date_posted':request.session['date_posted'],
            'program_owner':request.session['program_owner'],
            'program_owner_position':request.session['program_owner_position'],
            'q1':request.session['q1'],
            'q2':request.session['q2'],
            'q3':request.session['q3'],
            'q4':request.session['q4'],
            'q5':request.session['q5'],
            'q6':request.session['q6'],
            'q7':request.session['q7'],
            'q8':request.session['q8'],
            'q18':request.session['q18'],
            'q19':request.session['q19'],
            'q20':request.session['q20'],
            'q21':request.session['q21'],
            'q22':request.session['q22'],
            'q23':request.session['q23'],
            'q24':request.session['q24'],
            'q25':request.session['q25'],
            'q26':request.session['q26'],
            'q27':request.session['q27'],
            "q1_mean":request.session['q1_mean'],
            "q2_mean":request.session['q2_mean'],
            "q3_mean":request.session['q3_mean'],
            "q4_mean":request.session['q4_mean'],
            "q5_mean":request.session['q5_mean'],
            "q6_mean":request.session['q6_mean'],
            "q7_mean":request.session['q7_mean'],
            "q8_mean":request.session['q8_mean'],
            "q18_mean":request.session['q18_mean'],
            "q19_mean":request.session['q19_mean'],
            "q20_mean":request.session['q20_mean'],
            "q21_mean":request.session['q21_mean'],
            "q22_mean":request.session['q22_mean'],
            "q23_mean":request.session['q23_mean'],
            "q24_mean":request.session['q24_mean'],
            "q25_mean":request.session['q25_mean'],
            "q26_mean":request.session['q26_mean'],
            "q27_mean":request.session['q27_mean'],
            "total_of_participants":request.session['total_of_participant'],
            "total_of_participants2":request.session['total_of_participant2'],
            "facilitator_response":request.session['facilitator_response'],
            "facilitator_mean":request.session['facilitator_mean'],
            "facilitator_topic":request.session['facilitator_topic'],
            "mean_1":request.session['mean_1'],
            "mean_2":request.session['mean_2'],
            "mean_3":request.session['mean_3'],
            "mean_4":request.session['mean_4'],
            "facilitator_question":request.session['facilitator_question'],
            "overall_mean":request.session['overall_mean'],
            "comments":request.session['comments']
            }
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="'+str(request.session['date_posted'])+'report.pdf"'
            # find the template and render it.
            template = get_template(template_path)
            html = template.render(context)

            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response, link_callback=link_callback)
            print("may error dito")
            # if error then show some funy view
            if pisa_status.err:
                print("may error")
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response    

def get_summary_data2(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            request.session['seminar_title'] = request.POST.get('seminar_title')
            request.session['date_posted'] = request.POST.get('date_posted')
            request.session['program_owner'] = request.POST.get('program_owner')
            request.session['program_owner_position'] = request.POST.get('program_owner_position')
            request.session['q1'] = json.loads(request.POST.get('q1'))
            request.session['q2'] = json.loads(request.POST.get('q2'))
            request.session['q3'] = json.loads(request.POST.get('q3'))
            request.session['q4'] = json.loads(request.POST.get('q4'))
            request.session['q5'] = json.loads(request.POST.get('q5'))
            request.session['q6'] = json.loads(request.POST.get('q6'))
            request.session['q7'] = json.loads(request.POST.get('q7'))
            request.session['q8'] = json.loads(request.POST.get('q8'))
            request.session['q18'] = json.loads(request.POST.get('q18'))
            request.session['q19'] = json.loads(request.POST.get('q19'))
            request.session['q20'] = json.loads(request.POST.get('q20'))
            request.session['q21'] = json.loads(request.POST.get('q21'))
            request.session['q22'] = json.loads(request.POST.get('q22'))
            request.session['q23'] = json.loads(request.POST.get('q23'))
            request.session['q24'] = json.loads(request.POST.get('q24'))
            request.session['q25'] = json.loads(request.POST.get('q25'))
            request.session['q26'] = json.loads(request.POST.get('q26'))
            request.session['q27'] = json.loads(request.POST.get('q27'))
            request.session['q1_mean'] = request.POST.get('q1_mean')
            request.session['q2_mean'] = request.POST.get('q2_mean')
            request.session['q3_mean'] = request.POST.get('q3_mean')
            request.session['q4_mean'] = request.POST.get('q4_mean')
            request.session['q5_mean'] = request.POST.get('q5_mean')
            request.session['q6_mean'] = request.POST.get('q6_mean')
            request.session['q7_mean'] = request.POST.get('q7_mean')
            request.session['q8_mean'] = request.POST.get('q8_mean')
            request.session['q18_mean'] = request.POST.get('q18_mean')
            request.session['q19_mean'] = request.POST.get('q19_mean')
            request.session['q20_mean'] = request.POST.get('q20_mean')
            request.session['q21_mean'] = request.POST.get('q21_mean')
            request.session['q22_mean'] = request.POST.get('q22_mean')
            request.session['q23_mean'] = request.POST.get('q23_mean')
            request.session['q24_mean'] = request.POST.get('q24_mean')
            request.session['q25_mean'] = request.POST.get('q25_mean')
            request.session['q26_mean'] = request.POST.get('q26_mean')
            request.session['q27_mean'] = request.POST.get('q27_mean')
            request.session['total_of_participant'] = request.POST.get('total_of_participants')
            request.session['total_of_participant2'] = request.POST.get('total_of_participants2')
            request.session['facilitator_response'] = json.loads(request.POST.get('facilitator_response'))
            request.session['facilitator_mean'] = json.loads(request.POST.get('facilitator_mean'))
            request.session['facilitator_topic'] = request.POST.get('facilitator_topic')
            request.session['mean_1'] = float(request.POST.get('mean_1'))
            request.session['mean_2'] = float(request.POST.get('mean_2'))
            request.session['mean_3'] = float(request.POST.get('mean_3'))
            request.session['mean_4'] = float(request.POST.get('mean_4'))
            request.session['facilitator_question'] = json.loads(request.POST.get('facilitator_question'))
            request.session['overall_mean'] = float(request.POST.get('overall_mean'))
            request.session['comments'] = json.loads(request.POST.get('comments'))
            return JsonResponse({"validation":"success"})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')
        
def view_seminar_information_ajax(request):
    current_id = request.POST.get('current_id')
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax and request.method == "POST":
        doc_ref = db.collection(u'evaluations').document(current_id).collection('evaluators')
        docs = doc_ref.get()
        evaluated = 0
        not_evaluated = 0
        for doc in docs:
            if doc.to_dict()['status'] == "evaluated":
                evaluated = evaluated + 1
            else:
                not_evaluated =  not_evaluated + 1
        print(evaluated)
        return JsonResponse({"evaluated": evaluated,"not_evaluated":not_evaluated}, status=200)
    return JsonResponse({'status': 'Invalid request'}, status=400)
    
