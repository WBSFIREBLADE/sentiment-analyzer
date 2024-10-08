from django.shortcuts import render, redirect
from django.contrib.auth import login, logout as l_a, authenticate
from .forms import UserRegistrationForm ,LoginRegisterForm
from transformers import pipeline
from .forms import TextInputForm, FileUploadForm
from .models import SentimentAnalysis  # If you're using the model

# Initialize sentiment analysis pipeline
sentiment_analyzer = pipeline('sentiment-analysis')




def register(request):
    if request.method == 'POST':  # Ensure the method is POST
        form = UserRegistrationForm(request.POST)  # Correct 'post' to 'POST'
        if form.is_valid():
            user = form.save(commit=False)  # Create user instance without saving
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()  # Save user to the database
            login(request, user)  # Log the user in after registration
            return redirect('analyze')  # Redirect to a home page or another page
    else:
        form = UserRegistrationForm()
    return render(request, 'sentiment_analysis_app/register.html', {'form': form})



def login_user(request):
    if request.method == 'POST':
        form = LoginRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)  # Authenticate the user
            if user is not None:
                login(request, user)  # Log the user in
                return redirect('analyze')  # Redirect to a home page or another page
            else:
                form.add_error(None, "Invalid username or password.")  # Add an error message
    else:
        form = LoginRegisterForm()
    return render(request, 'sentiment_analysis_app/login.html', {'form': form})

def logout(request):
    l_a(request)
    return redirect('home') 


def analyze_sentiment(request):
    # Redirect to login if user is not authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Replace 'login' with your login URL name

    result = None
    history = []

    if request.method == 'POST':
        # Check if text input form is submitted
        text_form = TextInputForm(request.POST)
        if text_form.is_valid():
            user_input = text_form.cleaned_data['text_input']
            analysis = sentiment_analyzer(user_input)[0]
            result = {
                'text': user_input,
                'sentiment': analysis['label'],
                'confidence': round(analysis['score'], 2)
            }
            # Optional: Save to database
            SentimentAnalysis.objects.create(
                user=request.user,  # Save the user
                text=user_input, 
                sentiment=analysis['label'], 
                confidence=analysis['score']
            )

        # Check if file upload form is submitted
        file_form = FileUploadForm(request.POST, request.FILES)
        if file_form.is_valid():
            uploaded_file = request.FILES['file']
            text = uploaded_file.read().decode('utf-8')
            analysis = sentiment_analyzer(text)[0]
            result = {
                'text': text,
                'sentiment': analysis['label'],
                'confidence': round(analysis['score'], 2)
            }
            # Optional: Save to database
            SentimentAnalysis.objects.create(
                user=request.user,  # Save the user
                text=text, 
                sentiment=analysis['label'], 
                confidence=analysis['score']
            )

    else:
        text_form = TextInputForm()
        file_form = FileUploadForm()

    return render(request, 'sentiment_analysis_app/analyze.html', {
        'text_form': text_form,
        'file_form': file_form,
        'result': result,
        'history': history,
    })

# Create your views here.
