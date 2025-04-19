from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import UploadDatasetForm
from .models import StudentData
from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
import pickle
import os

# Load or Initialize the ML model
model = None
model_file = 'mainapp/ml_model.pkl'

# Load pre-trained model if exists
if os.path.exists(model_file):
    with open(model_file, 'rb') as f:
        model = pickle.load(f)

# Home page (shows Home/Upload/Register/Login links)
def home(request):
    return render(request, 'home.html')

# About page (project abstract and features)
def about(request):
    return render(request, 'about.html')

# Register New User
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        if password == confirm_password:
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('login')
        else:
            return render(request, 'register.html', {'error': 'Passwords do not match!'})
    return render(request, 'register.html')

# Login User
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('input_data')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

# Logout User
def logout_view(request):
    logout(request)
    return redirect('/')

# Upload Dataset
#from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def upload_dataset(request):
    global model
    if request.method == 'POST':
        dataset = request.FILES['dataset']
        df = pd.read_csv(dataset)
        
        X = df[['pss', 'psqi', 'sleep', 'activities']]
        y = df['stress_level']

        model = GradientBoostingClassifier()
        model.fit(X, y)

        # Save model
        with open('mainapp/ml_model.pkl', 'wb') as f:
            pickle.dump(model, f)

        # Calculate scores and store in session
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        y_pred = model.predict(X)

        request.session['acc'] = round(accuracy_score(y, y_pred) * 100, 2)
        request.session['prec'] = round(precision_score(y, y_pred, average='macro') * 100, 2)
        request.session['rec'] = round(recall_score(y, y_pred, average='macro') * 100, 2)
        request.session['f1'] = round(f1_score(y, y_pred, average='macro') * 100, 2)

        # Render upload page again with success message
        return render(request, 'upload_dataset.html', {'success': True})

    return render(request, 'upload_dataset.html')



# Input Data for Prediction
def input_data(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        pss_score = int(request.POST['pss_score'])
        psqi_score = int(request.POST['psqi_score'])
        sleep_hours = float(request.POST['sleep_hours'])
        activities_hours = int(request.POST['activities_hours'])

        prediction = model.predict([[pss_score, psqi_score, sleep_hours, activities_hours]])[0]

        # Save student's data
        StudentData.objects.create(
            student=request.user,
            pss_score=pss_score,
            psqi_score=psqi_score,
            sleep_hours=sleep_hours,
            activities_hours=activities_hours,
            prediction_result=prediction
        )

        # Save to session to show in result page
        request.session['data'] = {
            'pss_score': pss_score,
            'psqi_score': psqi_score,
            'sleep_hours': sleep_hours,
            'activities_hours': activities_hours
        }
        request.session['result'] = prediction

        return redirect('result')

    return render(request, 'input_data.html')

# Result Page
def result(request):
    if not request.user.is_authenticated:
        return redirect('login')

    data = request.session.get('data')
    result = request.session.get('result')

    # Metrics
    acc = request.session.get('acc', None)
    prec = request.session.get('prec', None)
    rec = request.session.get('rec', None)
    f1 = request.session.get('f1', None)

    return render(request, 'result.html', {
        'data': data,
        'result': result,
        'acc': acc,
        'prec': prec,
        'rec': rec,
        'f1': f1,
    })
