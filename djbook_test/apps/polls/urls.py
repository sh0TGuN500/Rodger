from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.home, name='home'),
    path('polls/personal_page/', views.personal_page, name='personal_page'),
    path('polls/', views.IndexView.as_view(), name='index'),
    path('polls/my_questions', views.MyQuestionsView.as_view(), name='my_questions'),
    path('polls/<int:pk>/', views.DetailMixinView.as_view(), name='detail'),
    path('polls/<int:pk>/results/', views.ResultView.as_view(), name='results'),
    path('polls/<int:question_id>/vote/', views.vote, name='vote'),
    path('polls/<int:question>/leave_comment/', views.AddComment.as_view(), name='leave_comment'),
    path('polls/add_question/', views.add_question, name='add_question'),
    path('polls/edit_question/<int:question_id>', views.add_question, name='edit_question'),
    path('polls/add_question/leave_question', views.leave_question, name='leave_question'),
    path('polls/edit_question/update_question/<int:question_id>', views.leave_question, name='update_question'),
    path('polls/search', views.search, name='search'),
    path('polls/delete_question/<int:question_id>', views.delete_question, name='delete_question')
]