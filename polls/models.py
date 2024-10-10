from django.db import models
from django.utils import timezone
import datetime

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True) 
    #auto_now를 True로 하면 qeustion이 업데이트 될 때마다 자동으로 날짜입력
    #auto_now_add를 Ture로 하면 생성될 때 날짜 자동입력

    def was_published_recently(self):
        #현재 시간에서 1일을 뺀 시간을 나타냅니다. 즉, 24시간 전의 시간을 구합니다.
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        if self.was_published_recently():
            new_badge = 'NEW!!!'
        else:
            new_badge = ''
        return f'{new_badge}퀴즈제목: {self.question_text}, 날짜: {self.pub_date}'
    
    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f'[{self.question.question_text}] : {self.choice_text}'