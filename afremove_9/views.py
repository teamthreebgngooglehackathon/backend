from django.shortcuts import render
from django.contrib import auth
from pyrebase import pyrebase

config = {
    'apiKey': "AIzaSyBxJTyBRe7bVkT_HaB6fHNxDc13mK-U8F8",
    'authDomain': "afremote-a775b.firebaseapp.com",
    'databaseURL': "https://afremote-a775b-default-rtdb.europe-west1.firebasedatabase.app",
    'projectId': "afremote-a775b",
    'storageBucket': "afremote-a775b.appspot.com",
    'messagingSenderId': "261676390679",
    'appId': "1:261676390679:web:99f87beb45060370fc3f52",
    'measurementId': "G-KN81XFM62P"
}

firebase = pyrebase.initialize_app(config)

autho = firebase.auth()

db = firebase.database()


def signIn(request):
    return render(request, "signIn.html")


def postsign(request):
    email = request.POST.get('email')
    password = request.POST.get('pass')
    try:
        user = autho.sign_in_with_email_and_password(email, password)
    except:
        message = "invalid credentials"
        return render(request, "signIn.html", {"messag": message})
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request, "welcome.html", {"e": email})


def logout(request):
    auth.logout(request)
    return render(request, "signIn.html")


def signup(request):
    return render(request, 'signup.html')


def postsignup(request):
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    email = request.POST.get('email')
    password = request.POST.get('pass')
    confirm_password = request.POST.get('confirm_pass')

    if password != confirm_password:
        message = "Passwords are not matching"
        return render(request, "signup.html", {"messag": message})

    user = autho.create_user_with_email_and_password(email, password)

    user_id = user['localId']
    account_data = {'firstname': firstname, 'lastname': lastname, 'email': email, 'password': password}

    db.child('Candidates').child(user_id).child('Account').set(account_data)

    return render(request, "signIn.html")


def push_education(request):
    return render(request, "education.html")


def post_push_education(request):
    school = request.POST.get('school')
    qualification = request.POST.get('qualification')
    field = request.POST.get('field')
    data = {
        'School': school,
        'Qualification': qualification,
        'Field': field
    }
    idtoken = request.session['uid']
    user_ = autho.get_account_info(idtoken)
    print(user_)
    hello_user = user_['users'][0]['localId']

    db.child('Candidates').child(hello_user).child("Education").set(data)

    # print(request.user)
    return render(request, "welcome.html")


def company_submit(request):
    return render(request, "company_submit.html")


def post_company_submit(request):
    values, keys = [], []
    company_name = request.POST.get("companyname")
    values.append(company_name)
    keys.append("companyname")
    industry = request.POST.get("industry")
    values.append(industry)
    keys.append("industry")
    deadline = request.POST.get("deadline")
    values.append(deadline)
    keys.append("deadline")
    position = request.POST.get("position")
    values.append(position)
    keys.append("position")

    phone = int(request.POST.get("phone"))
    values.append(phone)
    keys.append("phone")
    remote = request.POST.get("remote")
    values.append(remote)
    keys.append("remote")
    jobdescription = request.POST.get("jobdescription")
    values.append(jobdescription)
    keys.append("jobdescription")
    jobrequirments = request.POST.get("jobrequirments")
    values.append(jobrequirments)
    keys.append("jobrequirments")

    data = {}

    for i in range(len(keys)):
        data[keys[i]] = values[i]

    db.child('Company').child(company_name).set(data)

    # data = {"company_name":company_name, "industry"}

    return render(request, "signIn.html")
