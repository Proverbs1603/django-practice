from django.urls import path
from . import views
from .views import SignupView

app_name = 'polls'
urlpatterns = [
    #나는 / 붙여야 되네.
    path('', views.index, name='index'),  #views 파일에 index 함수로 가세요(컨트롤러)
    path('/<int:question_id>/', views.detail, name='detail'),
    path('/<int:question_id>/vote/', views.vote, name='vote'),
    path('/<int:question_id>/result', views.result, name='result'),
    path('/singup/', SignupView.as_view()),
]
