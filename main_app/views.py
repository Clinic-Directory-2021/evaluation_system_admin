from logging import ERROR, error
from django.http.response import HttpResponse
import firebase_admin
from django.shortcuts import render,redirect
from firebase_admin import credentials
from firebase_admin import firestore
import pyrebase
from datetime import datetime
import calendar
import time
from django.http import JsonResponse, request
import xlwt

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
cred = credentials.Certificate("main_app\ServiceAccountKey.json")
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
    doc_ref = db.collection(u'admins').document(request.session.get('admin_id'))
    doc = doc_ref.get()
    if doc.exists:
        open_seminar = db.collection(u'seminars').get()
        seminar_dict = {
        }
        for seminar in open_seminar:
            # seminar_id = u'{}'.format(seminar.to_dict()['seminar_id'])
            return render(request,'dashboard.html', {'full_name': doc.to_dict,"seminar_data":[seminar.to_dict() for seminar in open_seminar]})
    else:
        print(u'No such document!')
        return render(request,'dashboard.html')
    return render(request,'dashboard.html')
    

def manage_seminar(request):
    docs = db.collection(u'seminars').get()
    seminar_id = {
        
    }
    ctr = 0
    for doc in docs:
        ctr = ctr + 1
        seminar_id[ctr] = doc.id 
        return render(request,'manage_seminar.html',{"seminar_data":[doc.to_dict() for doc in docs]})
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
    docs = db.collection(u'evaluators').get()
    evaluator_id = {
        
    }
    ctr = 0
    for doc in docs:
        ctr = ctr + 1
        evaluator_id[ctr] = doc.id 
        return render(request,'manage_evaluator.html',{"evaluator_data":[doc.to_dict() for doc in docs],"evaluator_id":id})
    return render(request, 'manage_evaluator.html')

def report(request):
    evaluation_report = db.collection(u'evaluation_report').get()
    seminar_report = db.collection(u'seminar_report').get()
    evaluator_report = db.collection(u'evaluator_report').get()
    facilitator_report = db.collection(u'facilitator_report').get()
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
    for doc in facilitator_report:
        facilitator_counter = facilitator_counter + 1
    return render(request, 'report.html',{"evaluation_counter":evaluation_counter,"seminar_counter":seminar_counter,"evaluator_counter":evaluator_counter,"facilitator_counter":facilitator_counter})

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
        print(current_id)
        evaluators = db.collection(u'evaluators').get()
        evaluator_count = 0;

        #Evaluator count
        for doc in evaluators:
            evaluator_count = evaluator_count + 1

        #Evaluation data
        evaluations = db.collection(u'evaluations').document(str(current_id))
        seminar = evaluations.get()
        seminar_name = u'{}'.format(seminar.to_dict()['seminar_name'])
        seminar_date_id = str(u'{}'.format(seminar.to_dict()['seminar_date_id']))
        seminar_id = u'{}'.format(seminar.to_dict()['seminar_id'])
        date = u'{}'.format(seminar.to_dict()['date'])


        evaluation_data = evaluations.collection(u'evaluators').get()
        for doc in evaluation_data:
            print(f'{doc.id} => {doc.to_dict()}')
            evaluator_id = str(doc.id)
            evaluation_count = 0
            if doc.exists:
                evaluation_count = evaluation_count + 1
                return render(request, 'view_seminar_information.html',{"seminar_name":seminar_name,"seminar_id":seminar_id,"seminar_date_id":seminar_date_id,"evaluation_data":[doc.to_dict()],"evaluation_count":evaluation_count,"evaluator_id":evaluator_id,"evaluator_count":evaluator_count,"date":date})
        else:
            print(u'No such document!')
    except:
        print('ssss')
    return render(request, 'view_seminar_information.html')

def edit_seminar(request):
    current_id = request.GET.get('current_id')
    request.session['current_id'] =  current_id
    doc_ref = db.collection(u'seminars').document(current_id)
    doc = doc_ref.get()
    seminar_name = u'{}'.format(doc.to_dict()['seminar_name'])
    facilitator = u'{}'.format(doc.to_dict()['facilitator'])
    status = u'{}'.format(doc.to_dict()['status'])

    facilitators = db.collection(u'facilitators').get()
    for facilitator_data in facilitators:
        return render(request,'edit_seminar.html',{"seminar_name":seminar_name,"facilitator":facilitator,"status":status,"facilitators":[facilitator_data.to_dict()]})
    
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
        address = u'{}'.format(doc.to_dict()['address'])
        phone_number = u'{}'.format(doc.to_dict()['phone_number'])
        birth_date = u'{}'.format(doc.to_dict()['birth_date'])

        return render(request,'edit_evaluator.html',{"first_name":first_name,"middle_name":middle_name,"last_name":last_name,"email":email,"gender":gender,"address":address,"phone_number":phone_number,"birth_date":birth_date})
    else:
        print('ssss')
    return render(request,'edit_evaluator.html')

def total_evaluations(request):
    docs = db.collection(u'evaluation_report').get()
    evaluation_id = {
        
    }
    ctr = 0
    for doc in docs:
        ctr = ctr + 1
        evaluation_id[ctr] = doc.id 
        return render(request,'total_evaluations.html',{"evaluation_data":[doc.to_dict() for doc in docs],"evaluation_id":id})
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
    docs = db.collection(u'evaluator_report').get()
    evaluator_id = {
        
    }
    ctr = 0
    for doc in docs:
        ctr = ctr + 1
        evaluator_id[ctr] = doc.id 
        return render(request,'total_evaluators.html',{"evaluator_data":[doc.to_dict() for doc in docs],"evaluator_id":id})
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
        seminar_name = u'{}'.format(seminar.to_dict()['seminar_name'])
        seminar_date_id = str(u'{}'.format(seminar.to_dict()['seminar_date_id']))
        seminar_id = u'{}'.format(seminar.to_dict()['seminar_id'])
        date = u'{}'.format(seminar.to_dict()['date'])


        evaluation_data = evaluations.collection(u'evaluators').get()
        for doc in evaluation_data:
            print(f'{doc.id} => {doc.to_dict()}')
            evaluator_id = str(doc.id)
            evaluation_count = 0
            if doc.exists:
                evaluation_count = evaluation_count + 1
                return render(request, 'report_view_evaluation_info.html',{"seminar_name":seminar_name,"seminar_id":seminar_id,"seminar_date_id":seminar_date_id,"evaluation_data":[doc.to_dict()],"evaluation_count":evaluation_count,"evaluator_id":evaluator_id,"date":date})
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
        address = u'{}'.format(doc.to_dict()['address'])
        phone_number = u'{}'.format(doc.to_dict()['phone_number'])
        birth_date = u'{}'.format(doc.to_dict()['birth_date'])

        return render(request,'report_view_evaluator.html',{"first_name":first_name,"middle_name":middle_name,"last_name":last_name,"email":email,"gender":gender,"address":address,"phone_number":phone_number,"birth_date":birth_date})
    else:
        print('ssss')
    return render(request,'report_view_evaluator.html')
#post backends
def postsignIn(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    try:
        # if there is no error then signin the user with given email and password
        user=authe.sign_in_with_email_and_password(email,password)
    except:
        message="Email or Password is incorrect."
        return render(request,"login.html",{"message":message})
    # session_id=user['idToken']
    request.session['admin_id'] =  user['localId']
    doc_ref = db.collection(u'admins').document(request.session.get('admin_id'))
    doc = doc_ref.get()
    if doc.exists:
        # request.session['uid']=str(session_id)  
        doc_ref = db.collection(u'admins').document(request.session.get('admin_id'))
        doc = doc_ref.get()
        if doc.exists:
            open_seminar = db.collection(u'seminars').get()
            seminar_dict = {
            }
            for seminar in open_seminar:
                #? seminar_id = u'{}'.format(seminar.to_dict()['seminar_id'])
                request.session['session'] = True
                return render(request,'dashboard.html', {'full_name': doc.to_dict,"seminar_data":[seminar.to_dict() for seminar in open_seminar]})
        else:
            print(u'No such document!')
    

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
        seminar_name = request.POST.get('seminar_name')
        facilitator = request.POST.get('facilitator')
        date_created = datetime.now()
        seminar_id =  calendar.timegm(date_created.timetuple())
        try:
            data = {
            u'seminar_name': seminar_name,
            u'facilitator': facilitator,
            u'date_created': date_created,
            u'status':"close",
            u'seminar_id':str(seminar_id),
            u'ongoing':"false"
            }
            db.collection(u'seminars').document(str(seminar_id)).set(data)
            db.collection(u'seminar_report').document(str(seminar_id)).set(data)
        except:
            return render(request,'add_seminar.html')
        docs = db.collection(u'seminars').get()
        seminar_id = {
            
        }
        ctr = 0
        for doc in docs:
            ctr = ctr + 1
            seminar_id[ctr] = doc.id 
            return render(request,'manage_seminar.html',{"seminar_data":[doc.to_dict() for doc in docs]})
        return render(request,'manage_seminar.html')

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
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        birth_date = request.POST.get('birth_date ')
        date_created = datetime.now()
        evaluator_id =  calendar.timegm(date_created.timetuple())
        try:
            data = {
            u'evaluator_id':str(evaluator_id),
            u'first_name': first_name ,
            u'middle_name': middle_name,
            u'last_name': last_name,
            u'email':email,
            u'gender': gender,
            u'address': address,
            u'phone_number': phone_number,
            u'birth_date':birth_date,
            u'date_created':date_created,
            }
            db.collection(u'evaluators').document(str(evaluator_id)).set(data)
            db.collection(u'evaluator_report').document(str(evaluator_id)).set(data)
        except:
            print('ssss')
            return render(request,'add_evaluator.html')
        docs = db.collection(u'evaluators').get()
        evaluator_id = {
            
        }
        ctr = 0
        for doc in docs:
            ctr = ctr + 1
            evaluator_id[ctr] = doc.id 
            return render(request,'manage_evaluator.html',{"evaluator_data":[doc.to_dict() for doc in docs],"evaluator_id":id})

def post_edit_seminar(request):
    try:
        current_id = request.session['current_id']
        seminar_name = request.POST.get('seminar_name')
        facilitator = request.POST.get('facilitator')
        status = request.POST.get('status')
        update_seminar = db.collection(u'seminars').document(current_id)
        updated_data = {
            u'seminar_name': seminar_name,
            u'facilitator':facilitator,
            u'status':status
            }
        update_seminar.update(updated_data)
        docs = db.collection(u'seminars').get()
        seminar_id = {
            
        }
        ctr = 0
        for doc in docs:
            ctr = ctr + 1
            seminar_id[ctr] = doc.id 
        return render(request,'manage_seminar.html',{"seminar_data":[doc.to_dict() for doc in docs]})
    except:
          return render(request,'edit_seminar.html')

def post_edit_facilitator(request):
    current_id = request.session['current_id']
    facilitator_name = request.POST.get('facilitator_name')
    department = request.POST.get('department')
    rate = request.POST.get('rate')
    update_seminar = db.collection(u'facilitators').document(current_id)
    updated_data = {
        u'facilitator_name': facilitator_name,
        u'department':department,
        u'rate':rate
        }
    update_seminar.update(updated_data)

    docs = db.collection(u'facilitators').get()
    seminar_id = {
        
    }
    ctr = 0
    for doc in docs:
        ctr = ctr + 1
        seminar_id[ctr] = doc.id 
    return render(request,'manage_facilitator.html',{"facilitator_data":[doc.to_dict() for doc in docs]})

def post_edit_evaluator(request):
    current_id = request.session['current_id']
    first_name = request.POST.get('first_name')
    middle_name = request.POST.get('middle_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    gender = request.POST.get('gender')
    phone_number = request.POST.get('phone_number')
    address = request.POST.get('address')
    birth_date = request.POST.get('birth_date')
    update_evaluator = db.collection(u'evaluators').document(current_id)
    updated_data = {
        u'first_name': first_name,
        u'middle_name':middle_name,
        u'last_name':last_name,
        u'email': email,
        u'gender':gender,
        u'phone_number':phone_number,
        u'address': address,
        u'birth_date':str(birth_date),
        }
    update_evaluator.update(updated_data)

    docs = db.collection(u'evaluators').get()
    evaluator_id = {
        
    }
    ctr = 0
    for doc in docs:
        ctr = ctr + 1
        evaluator_id[ctr] = doc.id 
        return render(request,'manage_evaluator.html',{"evaluator_data":[doc.to_dict() for doc in docs],"evaluator_id":id})
    return render(request,'manage_evaluator.html')

def post_start_seminar(request):
    current_id = request.POST.get('seminar_id')
    seminar_document = db.collection(u'seminars').document(current_id)
    seminar_document.update({u'ongoing': "true"})
    seminar_document.update({u'status': "open"})
    docs = db.collection(u'seminars').get()
    seminar_docs =  seminar_document.get()
    seminar_name = u'{}'.format(seminar_docs.to_dict()['seminar_name'])
    date_created = datetime.now()
    seminar_date_id = calendar.timegm(date_created.timetuple())
    seminar_id = {
        
    }
    ctr = 0

    data = {
    u'date': date_created,
    u'seminar_date_id': seminar_date_id,
    u'seminar_id': current_id,
    u'seminar_name':seminar_name
    }
    default = {
        "default":""
    }
    print(seminar_date_id)
    evaluations_collection = db.collection(u'evaluations').document(current_id)
    evaluations_collection.set(data)
    evaluations_collection.collection('evaluators').document('evaluator_id').set(default)
    for doc in docs:
        ctr = ctr + 1
        seminar_id[ctr] = doc.id 
        return render(request,'manage_seminar.html',{"seminar_data":[doc.to_dict() for doc in docs]})
    return render(request,'manage_seminar.html')

def post_view_seminar_actions(request):
    #POST VALUES      
            seminar_date_id = request.POST.get('seminar_date_id')
            seminar_id = request.POST.get('seminar_id')
            evaluator_id = request.POST.get('evaluator_id')
            seminar_name = request.POST.get('seminar_name')
            date_created = request.POST.get('date')
            evaluation_report_field = {
                'date': date_created,
                "seminar_date_id":seminar_date_id,
                "seminar_id":seminar_id,
                "seminar_name":seminar_name
            }

    #Evaluation Report collection creation
            evaluation_report = db.collection(u'evaluation_report').document(seminar_id) 
            evaluation_report.set(evaluation_report_field)
            evaluations = evaluation_report.collection('evaluators').document(evaluator_id)

    #Evaluationlist traversion
            evaluations_list = db.collection(u'evaluations').document(seminar_id)
            evaluation_sub = evaluations_list.collection('evaluators').document(evaluator_id)
            get_data = evaluation_sub.get()
            if get_data.exists:
                #Set data of evaluation report
                evaluations.set(get_data.to_dict())
    #Deleting seminar after closing
            db.collection(u'seminars').document(seminar_id).delete()
            # update_seminar = db.collection(u'seminars').document(seminar_id)
            # update_seminar.update({u'ongoing': "false"})
            # update_seminar.update({u'status': u'close'})

    #Calling again the seminars in dashboard
            doc_ref = db.collection(u'admins').document(request.session.get('admin_id'))
            doc = doc_ref.get()
            if doc.exists:
                open_seminar = db.collection(u'seminars').get()
                seminar_dict = {
                }
                for seminar in open_seminar:
                    #? seminar_id = u'{}'.format(seminar.to_dict()['seminar_id'])
                    return render(request,'dashboard.html', {'full_name': doc.to_dict,"seminar_data":[seminar.to_dict() for seminar in open_seminar]})
            else:
                print(u'No such document!')
            return render(request,'dashboard.html')

def delete_seminar(request):
    current_id = request.GET.get('current_id')
    db.collection(u'seminars').document(current_id).delete()
    docs = db.collection(u'seminars').get()
    seminar_id = {
        
    }
    ctr = 0
    for doc in docs:
        ctr = ctr + 1
        seminar_id[ctr] = doc.id 
        return render(request,'manage_seminar.html',{"seminar_data":[doc.to_dict() for doc in docs]})
    return render(request,'manage_seminar.html')

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
    current_id = request.GET.get('current_id')
    db.collection(u'evaluators').document(current_id).delete()
    docs = db.collection(u'evaluators').get()
    evaluator_id = {
        
    }
    ctr = 0
    for doc in docs:
        ctr = ctr + 1
        evaluator_id[ctr] = doc.id 
        return render(request,'manage_evaluator.html',{"evaluator_data":[doc.to_dict() for doc in docs],"evaluator_id":id})
    return render(request, 'manage_evaluator.html')

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
               'Exhibited full grasp of the topic',
               'Was sensitive to the participants mood',
               'Asked stimulating questions',
               'Processed questions and responses to deepen learning',
               'Maintained positive learning environment',
               'Expressed ideas clearly',
               'Used appropriate training aids',
               'Observed appropriate attire',
               'Was able to firm up attainment of objectives of the session',
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
        rows = {
            str(0): counter + 1,
            str(1): u'{}'.format(doc.to_dict()['date']),
            str(2): u'{}'.format(doc.to_dict()['email']),
            str(3): u'{}'.format(doc.to_dict()['full_name']),
            str(4): u'{}'.format(doc.to_dict()['q1']),
            str(5): u'{}'.format(doc.to_dict()['q2']),
            str(6): u'{}'.format(doc.to_dict()['q3']),
            str(7): u'{}'.format(doc.to_dict()['q4']),
            str(8): u'{}'.format(doc.to_dict()['q5']),
            str(9): u'{}'.format(doc.to_dict()['q6']),
            str(10): u'{}'.format(doc.to_dict()['q7']),
            str(11): u'{}'.format(doc.to_dict()['q8']),
            str(12): u'{}'.format(doc.to_dict()['q9']),
            str(13): u'{}'.format(doc.to_dict()['q10']),
            str(14): u'{}'.format(doc.to_dict()['q11']),
            str(15): u'{}'.format(doc.to_dict()['q12']),
            str(16): u'{}'.format(doc.to_dict()['q13']),
            str(17): u'{}'.format(doc.to_dict()['q14']),
            str(18): u'{}'.format(doc.to_dict()['q15']),
            str(19): u'{}'.format(doc.to_dict()['q16']),
            str(20): u'{}'.format(doc.to_dict()['q17']),
            str(21): u'{}'.format(doc.to_dict()['q18']),
            str(22): u'{}'.format(doc.to_dict()['q19']),
            str(23): u'{}'.format(doc.to_dict()['q20']),
            str(24): u'{}'.format(doc.to_dict()['q21']),
            str(25): u'{}'.format(doc.to_dict()['q22']),
            str(26): u'{}'.format(doc.to_dict()['q23']),
            str(27): u'{}'.format(doc.to_dict()['q24']),
            str(28): u'{}'.format(doc.to_dict()['q25']),
            str(29): u'{}'.format(doc.to_dict()['q26']),
            str(30): u'{}'.format(doc.to_dict()['q27']),
            str(31): u'{}'.format(doc.to_dict()['c1']),
            str(32): u'{}'.format(doc.to_dict()['c2']),
            str(33): u'{}'.format(doc.to_dict()['c3']),
            str(34): u'{}'.format(doc.to_dict()['c4']),
        }
        row_num += 1
        for col_num in range(len(rows)):
            ws.write(row_num, col_num, rows.get(str(col_num)))
    wb.save(response)
    return response