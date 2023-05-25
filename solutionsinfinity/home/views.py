from django.shortcuts import render,redirect
from . models import *
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
# Create your views here.

#  return redirect('question_detail', pk=new_question.pk)
def index(request):
    questions = Question.objects.annotate(num_solutions=Count('solutions')).order_by('-num_solutions')
    context={"top_questions":questions}
    return render(request,'index.html',context)
def all_questions(request):
    questions= questions = Question.objects.annotate(num_solutions=Count('solutions')).order_by('-asked_at')
    tags=Tags.objects.all()
   
    
    context={"top_questions":questions,'tags':tags}
    return render(request,'all_questions.html',context)

@login_required(login_url="/login")
def user_home(request):
    user1=request.user
    user=User_details.objects.get(user=user1)
    
    tags=user.watched_tags.all()
    questions = Question.objects.filter(tags__in=user.watched_tags.all())
    display=questions.annotate(num_solutions=Count('solutions')).order_by('-num_solutions')
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-timestamp')


    
    context={"top_questions":display,'notifications': notifications,'tags':tags}
    print(display)
    return render(request,'user_home.html',context)


@login_required(login_url="http://127.0.0.1:8000/login")
def ask_question(request):
    if request.method == "POST":
        title=request.POST["title"]
        desc=request.POST["desc"]
        tag=request.POST.getlist('tags')
        user=request.user
        if "image1" in request.FILES:
            image1=request.FILES["image1"]
        else:
            image1=None
        if "image2" in request.FILES:
            image2=request.FILES["image2"]
        else:
            image2=None
        


        new=Question.objects.create(title=title,description=desc,asked_by=user)
        if image1:
            new.image1=image1
        if image2:
            new.image2=image2
        
        user_detail=User_details.objects.get(user=user)
        user_detail.reputation+=100
        user_detail.save()
        new.save()
        new.tags.set(tag)
        return redirect("/all_questions")

    else:
        tags=Tags.objects.all()
        context={'tags':tags}
        return render(request,'askquestion.html',context)

def register(request):
     if request.method == "POST":
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        mobile=request.POST['mobile']
        selected_tags = request.POST.getlist('tags')
       
        
        
        if password1 == password2:
            if User.objects.filter(username=username):
                messages.info(request,"Username already exist please choose another")
                return redirect("/register")
            elif User.objects.filter(email=email):
                messages.info(request,"Email Taken Please choose another")
                return redirect("/register")
            
            
            else:
                user=User.objects.create_user(username=username,email=email,password=password1)
                user.save()
                
                user_model=User.objects.get(username=username)
                id_usr=user_model.id
                new_profile = User_details(user=user_model, first_name=fname, last_name=lname, mobile=mobile)

                tags = Tags.objects.filter(id__in=selected_tags)
                new_profile.save()

                new_profile.watched_tags.add(*tags)
                messages.success(request,"Registered Succesfully ,Please Login")
                return redirect("/login")
        else:
            messages.info(request,"password not matching")
            return redirect("/register")
    
     else:
        tag=Tags.objects.all()
        return render(request,'register2.html',{'tags':tag})

    


def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("/user_home")
       
        else:
            messages.info(request,"Invalid Username or Password")
            return redirect("/login")
    else:
        return render(request,'login2.html')
    
@login_required(login_url="/login")
def logout(request):
    auth.logout(request)
    return redirect("/")

@login_required(login_url="/login")
def user_tags(request):
    user=request.user
    user_det=User_details.objects.get(user=user)
    user_tag=user_det.watched_tags.all()
    print(user_tag)
    watched=[]
    for i in user_tag:
        watched.append(i)
    print(watched)
    tags_queryset = Tags.objects.exclude(id__in=user_tag.values_list('id', flat=True))
    print(tags_queryset)
    if request.method == "POST":
        selected_tags = request.POST.getlist('tags')
        tags = Tags.objects.filter(id__in=selected_tags)
        user_det.watched_tags.add(*tags)
        return redirect("/user_tags")
        
    else:
        context={'user_tag':user_tag,'tags':tags_queryset}
        return render(request,'user_tags.html',context)
@login_required(login_url="/login")   
def remove_tag(request,pk):
    tag=Tags.objects.get(id=pk)
    user=request.user
    user_det=User_details.objects.get(user=user)
    user_det.watched_tags.remove(tag)
    return redirect("/user_tags")



def question_detail(request,pk):
    question=Question.objects.get(id=pk)
    solutions=Solutions.objects.filter(question=question).order_by('-upvotes')
    question_comment=Question_comments.objects.filter(question=question)
    user=request.user
    if request.method == "POST" and 'solution' in request.POST :
        title=request.POST["title"]
        answer=request.POST["answer"]
        if "image1" in request.FILES:
            image1=request.FILES["image1"]
        else:
            image1=None
        if "image2" in request.FILES:
            image2=request.FILES["image2"]
        else:
            image2=None
        

        new=Solutions.objects.create(question=question,title=title,solution=answer,answered_by=user)
        user_detail=User_details.objects.get(user=user)
        user_detail.reputation+=150
        user_detail.save()
        
        if image1:
            new.image1=image1
        if image2:
            new.image2=image2
        new.save()
        asked_by = question.asked_by
        message = f"A new solution for the question '{question.title}' has been added by {user.username}"
        notification = Notification(user=asked_by, message=message, timestamp=timezone.now())
        notification.save()
        # notify(recipient=asked_by, verb=message, target=question)
        return redirect("/question-detail/"+ str(pk))
    elif request.method == "POST" and "qn-com" in request.POST:
        comment=request.POST["comment"]
        new_qn_comment=Question_comments.objects.create(comment=comment,comment_by=user,question=question)
        new_qn_comment.save()
        return redirect("/question-detail/"+ str(pk))

    else:
        context={'question':question,'solutions':solutions,'question_comments':question_comment}
        return render(request,'question_detail2.html',context)
@login_required(login_url="/login")
def like(request,pk):
    user=request.user
    solution=Solutions.objects.get(id=pk)
    qn=request.GET["question"]
    print(qn)
    like_filter = upvote.objects.filter(solution=solution,user=user).first()
    if like_filter == None:
        #the user had not liked the button So that now user likes it
        new_like=upvote.objects.create(user=user,solution=solution)
        asked=solution.answered_by
        user_detail=User_details.objects.get(user=asked)
        user_detail.reputation+=200
        user_detail.save()
        new_like.save()
        solution.upvotes=solution.upvotes+1
        solution.save()
        
    else:
        #that user had already liked the post so dislike it
        like_filter.delete()
        solution.upvotes=solution.upvotes-1
        solution.save()
    return redirect("/question-detail/"+ str(qn))


def mark_as_read(request, pk):
    notification = Notification.objects.get(id=pk)
    notification.is_read = True
    notification.save()
    return redirect('/user_home')

def mark_all_as_read(request):
    user = request.user
    notifications = Notification.objects.filter(user=user, is_read=False)
    for notification in notifications:
        notification.is_read = True
        notification.save()
    return redirect('/user_home')

def all_tags(request):
    tags=Tags.objects.annotate(num_questions=Count('question'))
    context={'tags':tags}
    return render(request,'all_tags.html',context)

def tag_questions(request,pk):
    tag=Tags.objects.get(id=pk)
    
    
    
    questions = tag.question_set.all()
    question_count = questions.count()
    display = questions.annotate(num_solutions=Count('solutions')).order_by('-num_solutions')
    context = {'tag': tag, 'questions': display,'no':question_count}
    return render(request, 'tag_questions.html', context)

def profile(request,pk):
    user=User.objects.get(username=pk)
    profile=User_details.objects.get(user=user)
    questions=Question.objects.filter(asked_by=user)
    no_q=len(questions)
    answers=Solutions.objects.filter(answered_by=user)
    no_an=len(answers)
    context={'profile':profile,'u':user,'no_q':no_q,'no_an':no_an,'questions':questions,'answers':answers}
    return render(request,'profile2.html',context)


def edit_profile(request):
    user=request.user
    profile=User_details.objects.get(user=user)
    if request.method == "POST":
        fname=request.POST["fname"]
        lname=request.POST["lname"]
        
        mobile=request.POST["mobile"]
        profile.first_name=fname
        profile.last_name=lname
  
        profile.mobile=mobile

        if "profile" in request.FILES:
            image1=request.FILES["profile"]
            profile.profile_image=image1
        profile.save()
        return redirect("http://127.0.0.1:8000/edit-profile")
        
    else:
        context={'profile':profile}
        return render(request,'edit_profile.html',context)
    


#admin interface
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import os 

import io
import base64
from datetime import datetime, timedelta


def chart(request):
    # Query to get the number of questions asked and solutions given over the last 7 days
    dates = [datetime.now().date() - timedelta(days=i) for i in range(7)]
    questions = [Question.objects.filter(asked_at__date=date).count() for date in dates]
    solutions = [Solutions.objects.filter(answerd_at__date=date).count() for date in dates]

    # Create a line chart using Matplotlib
    fig, ax = plt.subplots()
    ax.plot(dates, questions, label='Questions Asked')
    ax.plot(dates, solutions, label='Solutions Given')
    ax.set_xlabel('Date')
    ax.set_ylabel('Count')
    ax.set_title('Questions Asked and Solutions Given')
    ax.legend()
    date_fmt = matplotlib.dates.DateFormatter('%d %b')
    ax.xaxis.set_major_formatter(date_fmt)
    image_path = 'reputation_bar_chart.png'
    static_path = os.path.join(settings.BASE_DIR, 'static')

    # Save the plot to a file in the static folder
    plt.savefig(os.path.join(static_path, 'chart.png'))
    

    # Render the HTML template with the chart image embedded
    return render(request, 'chart.html')

def line_chart_view(request):
    # Calculate the date range for the last 7 days
    today = datetime.now().date()
    last_week = today - timedelta(days=6)

    # Query the database for questions asked within the date range
    questions = Question.objects.filter(asked_at__date__range=[last_week, today])

    # Query the database for solutions given within the date range
    solutions = Solutions.objects.filter(answerd_at__date__range=[last_week, today])

    # Prepare the data for the line graph
    labels = [last_week + timedelta(days=i) for i in range(7)]
    questions_data = [questions.filter(asked_at__date=date).count() for date in labels]
    solutions_data = [solutions.filter(answerd_at__date=date).count() for date in labels]

    # Pass the data to the template for rendering
    context = {
        'labels': labels,
        'questions_data': questions_data,
        'solutions_data': solutions_data
    }
    return render(request, 'chart2.html', context)
    # Get the date range for the last 7 days
   
   


def reputation_bar_chart(request):
    users = User_details.objects.all()
    reputation_values = [user.reputation for user in users]
    usernames = [user.first_name for user in users]
    print(os.getcwd())


    fig, ax = plt.subplots()
    ax.bar(usernames, reputation_values)
    ax.set_xlabel('Usernames')
    ax.set_ylabel('Reputation')
    ax.set_title('Reputation of all users')
    image_path = 'reputation_bar_chart.png'
    static_path = os.path.join(settings.BASE_DIR, 'static')

    # Save the plot to a file in the static folder
    plt.savefig(os.path.join(static_path, 'reputation_bar_chart.png'))
    

    # Save the plot to a file
    context = {
        'image_path': os.path.abspath(image_path)
    }

    return render(request, 'reputation_bar_chart.html', context)

def user_chart(request):
    user_details = User_details.objects.all().order_by('-reputation')  # Retrieve user details ordered by reputation
    user_labels = [user.first_name for user in user_details]  # Extract user first names as labels
    user_reputations = [user.reputation for user in user_details]  # Extract user reputations

    context = {
        'user_labels': user_labels,
        'user_reputations': user_reputations,
    }

    return render(request, 'reputation_bar_chart2.html', context)



def search(request):
    query = request.POST.get('search')
    
    questions = Question.objects.filter(title__icontains=query) | Question.objects.filter(description__icontains=query)
   
    context = {
        'questions': questions,
        'query': query,
    }
    return render(request, 'search.html', context)


def delete_qn(request,pk):
    user=request.user
    r=f"http://127.0.0.1:8000/profile/{user}"
    try:
        question=Question.objects.get(id=pk)
    except:
        return redirect(r)
    question.delete()
    return redirect(r)


def delete_ans(request,pk):
    user=request.user
    r=f"http://127.0.0.1:8000/profile/{user}"
    try:
        ans=Solutions.objects.get(id=pk)
    except:
        return redirect(r)
    ans.delete()
    return redirect(r)