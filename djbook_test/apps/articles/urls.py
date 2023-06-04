from django.urls import path, include
from rest_framework import routers

from . import views, rest_views

app_name = 'articles'


router = routers.DefaultRouter()
router.register(r'articles', rest_views.ArticlesViewSet)
router.register(r'comments', rest_views.CommentsViewSet)
router.register(r'tags', rest_views.TagsViewSet)
router.register(r'votes', rest_views.VotesViewSet)
router.register(r'choices', rest_views.ChoicesViewSet)
router.register(r'article_likes', rest_views.ArticleLikeViewSet)
router.register(r'comment_likes', rest_views.CommentLikeViewSet)


urlpatterns = [
    path('api-root/', include(router.urls), name='api-root'),
    path('', views.home, name='home'),
    path('articles/personal_page/', views.personal_page, name='personal_page'),
    path('articles/', views.ArticleIndexView.as_view(), name='index'),
    path('articles/<int:tag_id>/', views.TagListView.as_view(), name='tag'),
    path('articles/my_articles/', views.MyArticlesView.as_view(), name='my_articles'),
    path('articles/<int:pk>', views.ArticleDetailView.as_view(), name='detail'),
    path('articles/<int:pk>/results/', views.VoteResultView.as_view(), name='results'),
    path('articles/article_like/<int:article_id>/<int:like>', views.article_like, name='article_like'),
    path('articles/comment_like/<int:comment_id>/<int:like>', views.comment_like, name='comment_like'),
    path('articles/<int:article_id>/vote/', views.vote, name='vote'),
    path('articles/<int:article_id>/comment_create/', views.CommentCreate.as_view(), name='comment_create'),
    path('articles/<int:article_id>/<int:comment_id>/comment_edit/', views.CommentCreate.as_view(), name='comment_edit'),
    path('articles/<int:article_id>/<int:comment_id>/comment_delete/', views.comment_delete, name='comment_delete'),
    path('articles/add_article/', views.article_create_update_form, name='article_create'),
    path('articles/add_article/create_article/', views.article_db_save, name='article_create_save'),
    path('articles/edit_article/<int:article_id>', views.article_create_update_form, name='article_update'),
    path('articles/edit_article/<int:article_id>/article_delete/', views.article_db_save, name='article_update_save'),
    path('articles/search/', views.ArticleSearchView.as_view(), name='search'),
    path('articles/delete_article/<int:article_id>', views.article_delete, name='article_delete'),
    path('about/', views.about, name='about'),
    path('language_switch/<str:user_language>/', views.lang_switcher, name='lang'),
    # path('articles/froala_form', views.froala_form, name='froala_form'),
    # path('articles/post_froala_form', views.post_froala_form, name='post_froala_form'),
    # path('articles/froala_index', views.FroalaIndexView.as_view(), name='froala_index'),
    # path('articles/froala/<int:pk>/', views.FroalaDetailMixinView.as_view(), name='froala_detail'),
    # path('ajax_demo/', views.AjaxHandlerView.as_view(), name='ajax_demo'),
    # path('ajax_page/', views.ajax_page, name='ajax_page'),
    # path('ajax_check/', views.AjaxDataCheck.as_view(), name='ajax_check')
]
