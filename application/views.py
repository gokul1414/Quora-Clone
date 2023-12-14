
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from application.forms import QuestionForm
from application.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def landing(request):
    return render(request, 'auth/login.html')
    

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def home(request):
    return render(request, 'auth/home.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)  
            question.user = request.user  
            question.save()  
            return redirect('home')  
    else:
        form = QuestionForm()
    return render(request, 'main/ask_question.html', {'form': form})


@login_required
def home(request):
    all_questions = Question.objects.all().order_by('-created_at')
    recent_questions = Question.objects.order_by('-created_at')[:3]

    questions_per_page = 10
    paginator = Paginator(all_questions, questions_per_page)
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    questions_count=all_questions.count()
    context = {
        'questions': questions,
        'questions_count':questions_count,
        'recent_questions':recent_questions
    }
    return render(request, 'main/home.html', context)

@login_required
def my_questions(request):
    user_id=request.user.id
    all_questions = Question.objects.filter(user_id=user_id).order_by('-created_at')
    questions_per_page = 10
    paginator = Paginator(all_questions, questions_per_page)
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    questions_count=all_questions.count()
    context = {
        'questions': questions,
        'questions_count':questions_count,
   
    }
    return render(request, 'main/my_questions.html', context)




@login_required
def question_detail(request, question_id):
    question = Question.objects.get(pk=question_id)
    answers = Answer.objects.filter(question=question).order_by('-created_at')
    recent_questions = Question.objects.filter(category=question.category).exclude(pk=question_id)[:3]
    questions_count=Question.objects.all().count()
    answers_count=Answer.objects.all().count()
    users_count=User.objects.all().count()
    answers_count_this=Answer.objects.filter(question_id=question_id).count()
    per_page = 5
    page = request.GET.get('page', 1)
    paginator = Paginator(answers, per_page)
    try:
        current_page_answers = paginator.page(page)
    except PageNotAnInteger:
        current_page_answers = paginator.page(1)
    except EmptyPage:
        current_page_answers = paginator.page(paginator.num_pages)
    context={
         'question': question,
          'answers': current_page_answers,
          'recent_questions':recent_questions,
          'questions_count':questions_count,
           'answers_count':answers_count,
           'users_count':users_count,
           'answers_count_this':answers_count_this
           }
    
    return render(request, 'main/question_details.html', context)


@login_required
def post_answer(request, question_id):
    if request.method == 'POST':
        content = request.POST.get('user_answer')
        question = Question.objects.get(pk=question_id)
        Answer.objects.create(user=request.user, question=question, content=content)
    return redirect('question_details', question_id=question_id)
