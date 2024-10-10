from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _

# Register your models here.

#StackedInline 은 세로방향 정렬
#TabularInline 은 가로방향 정렬
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3  #3개의 추가할 빈 choice 입력칸이 default로 나옴.


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('question_text', {'fields': ['question_text'], 'description': ['퀘스천']}),
        ('pub_data', {'fields': ['pub_date'], 'classes': ['collapse']}),        
    ]
    readonly_fields = ['pub_date'] #읽기모드 *auto_now_add = True 조건이면.
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently') #admin 목록 페이지에 나오는 것들.
    list_filter = ['pub_date'] #필터옵션제공 
    search_fields = ['question_text', 'choice__choice_text'] #question_text 또는 choice_text에 따라 검색 가능

admin.site.register(Question, QuestionAdmin)


'''
inlines 옵션으로 question에서 choice까지 생성 가능하므로 choice는 register하지 않아도 됨.
admin.site.register(Choice)
'''