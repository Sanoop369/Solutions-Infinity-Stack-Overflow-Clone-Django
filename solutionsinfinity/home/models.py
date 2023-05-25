from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import Truncator

# Create your models here.
User=get_user_model()

class Tags(models.Model):

    name=models.CharField(max_length=100)
    description=models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Question(models.Model):
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=200)
    asked_by=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    asked_at=models.DateTimeField(auto_now_add=True)
    tags=models.ManyToManyField(Tags)
    image1=models.ImageField(upload_to='questions', null=True)
    image2=models.ImageField(upload_to='questions', null=True)


    def __str__(self):
        return self.title
    def increase_reputation_on_question_asked(self):
        self.asked_by.user_details.reputation += 100
        self.asked_by.user_details.save()


class Solutions(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    title=models.CharField(max_length=100,null=True)
    solution=models.CharField(max_length=200)
    upvotes=models.IntegerField(default=0)
    answerd_at=models.DateTimeField(auto_now_add=True)
    answered_by=models.ForeignKey(User,on_delete=models.CASCADE)
    image1=models.ImageField(upload_to='solutions', null=True)
    image2=models.ImageField(upload_to='solutions', null=True)

    def __str__(self):
        x=Truncator(self.solution).chars(15)
        return x
    def increase_reputation_on_answered(self):
        self.answered_by.user_details.reputation += 150
        self.answered_by.user_details.save()


class User_details(models.Model):
    email = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='profile', null=True,default='blank_profile.png')
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    watched_tags=models.ManyToManyField(Tags)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=100,null=True)

    reputation = models.IntegerField(default=0)


    def __str__(self):
        return self.first_name



class Solution_comments(models.Model):
    comment=models.CharField(max_length=1000)
    comment_by=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    solution=models.ForeignKey(Solutions,on_delete=models.CASCADE)
    commented_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment_by.get_username + ":" + self.commented_at

class Question_comments(models.Model):
    comment=models.CharField(max_length=1000)
    comment_by=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    commented_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment_by.get_username + ":" + self.commented_at

class Admin_login(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    def __str__(self):
        return self.username
    
class upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    solution = models.ForeignKey(Solutions, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.get_username()} likes solution {self.solution.id}'
    
    def increase_reputation_on_upvoted(self):
        self.user.user_details.reputation += 200
        self.user.user_details.save()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.get_username()} notification on {self.timestamp}' 