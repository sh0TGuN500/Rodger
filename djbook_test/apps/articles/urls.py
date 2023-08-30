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
    path('personal_page/', views.personal_page, name='personal_page'),
    path('', views.ArticleIndexView.as_view(), name='index'),
    path('<int:tag_id>/', views.TagListView.as_view(), name='tag'),
    path('my_articles/', views.MyArticlesView.as_view(), name='my_articles'),
    path('<int:pk>', views.ArticleDetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.VoteResultView.as_view(), name='results'),
    path('article_like/<int:article_id>/<int:like>', views.article_like, name='article_like'),
    path('comment_like/<int:comment_id>/<int:like>', views.comment_like, name='comment_like'),
    path('<int:article_id>/vote/', views.vote, name='vote'),
    path('<int:article_id>/comment_create/', views.CommentCreate.as_view(), name='comment_create'),
    path('<int:article_id>/<int:comment_id>/comment_edit/', views.CommentCreate.as_view(), name='comment_edit'),
    path('<int:article_id>/<int:comment_id>/comment_delete/', views.comment_delete, name='comment_delete'),
    path('add_article/', views.article_create_update_form, name='article_create'),
    path('add_article/create_article/', views.article_db_save, name='article_create_save'),
    path('edit_article/<int:article_id>', views.article_create_update_form, name='article_update'),
    path('edit_article/<int:article_id>/article_delete/', views.article_db_save, name='article_update_save'),
    path('search/', views.ArticleSearchView.as_view(), name='search'),
    path('delete_article/<int:article_id>', views.article_delete, name='article_delete'),
    path('<int:article_id>/publish_article/', views.publish_article, name='publish_article'),
    # path('froala_form', views.froala_form, name='froala_form'),
    # path('post_froala_form', views.post_froala_form, name='post_froala_form'),
    # path('froala_index', views.FroalaIndexView.as_view(), name='froala_index'),
    # path('froala/<int:pk>/', views.FroalaDetailMixinView.as_view(), name='froala_detail'),
    # path('ajax_demo/', views.AjaxHandlerView.as_view(), name='ajax_demo'),
    # path('ajax_page/', views.ajax_page, name='ajax_page'),
    # path('ajax_check/', views.AjaxDataCheck.as_view(), name='ajax_check')
]
