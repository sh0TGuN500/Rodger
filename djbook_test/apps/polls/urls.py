from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.home, name='home'),
    path('polls/personal_page/', views.personal_page, name='personal_page'),
    path('polls/', views.QuestionIndexView.as_view(), name='index'),
    path('polls/<int:tag_id>', views.TagListView.as_view(), name='tag'),
    path('polls/my_questions', views.MyQuestionsView.as_view(), name='my_questions'),
    path('polls/<int:pk>/', views.QuestionDetailMixinView.as_view(), name='detail'),
    path('polls/<int:pk>/results/', views.VoteResultView.as_view(), name='results'),
    path('polls/<int:question_id>/vote/', views.vote, name='vote'),
    path('polls/<int:question_id>/comment_create/', views.CommentCreate.as_view(), name='comment_create'),
    path('polls/<int:question_id>/<int:comment_id>/comment_edit/', views.CommentCreate.as_view(), name='comment_edit'),
    path('polls/<int:question_id>/<int:comment_id>/comment_delete/', views.comment_delete, name='comment_delete'),
    path('polls/add_question/', views.question_create_update_form, name='create_question'),
    path('polls/add_question/create_question', views.question_db_save, name='create_question_save'),
    path('polls/edit_question/<int:question_id>', views.question_create_update_form, name='update_question'),
    path('polls/edit_question/<int:question_id>/update_question/', views.question_db_save, name='update_question_save'),
    path('polls/search', views.QuestionSearchView.as_view(), name='search'),
    path('polls/delete_question/<int:question_id>', views.question_delete, name='delete_question'),
    path('info_for_customers/', views.info_for_customers, name='info_for_customers')
    # path('polls/froala_form', views.froala_form, name='froala_form'),
    # path('polls/post_froala_form', views.post_froala_form, name='post_froala_form'),
    # path('polls/froala_index', views.FroalaIndexView.as_view(), name='froala_index'),
    # path('polls/froala/<int:pk>/', views.FroalaDetailMixinView.as_view(), name='froala_detail'),
    # path('ajax_demo/', views.AjaxHandlerView.as_view(), name='ajax_demo'),
    # path('ajax_page/', views.ajax_page, name='ajax_page'),
    # path('ajax_check/', views.AjaxDataCheck.as_view(), name='ajax_check')
]
