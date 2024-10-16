from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


def index(request):
    #order_by('-pub_date') 는 내림차순 정렬 가장 최근의 항목부터 가장 오래된 것
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #context = {'first_question' : latest_question_list[0]}
    context = {'questions' : latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    """
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    """
    question = get_object_or_404(Question, pk=question_id) #단점이 메시지를 못보내네
    context = {"question" : question}
    return render(request, "polls/detail.html", context)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    #인풋 name이 choice라서 request의 POST에 choice가 전달됨.
    try:
        selected_choice = question.choices.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question' : question,
                                                     'error_message' : '선택이 없습니다.'})
    else:
        # A서버에서도 Votes = 1
        # B서버에서도 Votes = 1, B나 A의 투표 중 하나는 묵시될 수 있음. 
        #서버가 아니라 DB에서 값을 읽어 변경해야함.
        #selected_choice.votes += 1
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:result', args=(question_id,)))
    
def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {"question" : question}
    return render(request, 'polls/result.html', context)

class SignupView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('user-list') #성공시 user-list 라는 name 가진 url로 redirect됨.
    template_name = 'registration/signup.html'
