from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('question/ask_question/',views.ask_question,name="ask_question"),
    path('question/<int:question_id>/', views.question_detail, name='question_details'),
    path('question/<int:question_id>/post_answer/', views.post_answer, name='post_answer'),
    path('my_questions/',views.my_questions,name='my_questions'),
]
