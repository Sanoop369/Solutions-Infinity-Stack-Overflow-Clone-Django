from django.urls import path,include
from . views import *
urlpatterns = [
    
    path('',index),
    path('register',register,name="register"),
    path('login',login,name="login"),
    path('user_home',user_home),
    path('logout',logout,name="logout"),
    path('user_tags',user_tags),
    path('remove-tag/<int:pk>',remove_tag),
    path('all_questions',all_questions,name="all_questions"),
    path('ask_question',ask_question,name="ask_question"),
    path('question-detail/<int:pk>',question_detail,name="question-detail"),
    path('like/<int:pk>',like,name="like"),
    path('mark-all-read',mark_all_as_read),
    path('mark-read/<int:pk>',mark_as_read),
    path('all_tags',all_tags),
    path('tag-question/<int:pk>',tag_questions,name="tag-question"),
    path('profile/<str:pk>',profile),
    path('edit-profile',edit_profile,name="edit-profile"),
    path('reputation_bar_chart/', user_chart, name='reputation_bar_chart'),
    path('chart',chart),
    path('search',search,name="search"),
    path('delete-qn/<int:pk>',delete_qn),
    path('delete-ans/<int:pk>',delete_ans),
   

]