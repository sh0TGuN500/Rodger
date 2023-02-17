import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Article


def create_article(article_text, days):
    """
    Create a article with the given `article_text` and published the
    given number of `days` offset to now (negative for articles published
    in the past, positive for articles that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Article.objects.create(article_text=article_text, pub_date=time)


class ArticleIndexViewTests(TestCase):
    def test_no_articles(self):
        """
        If no articles exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('articles:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No articles are available.")
        self.assertQuerysetEqual(response.context['latest_article_list'], [])

    def test_past_article(self):
        """
        Articles with a pub_date in the past are displayed on the
        index page.
        """
        create_article(article_text="Past article.", days=-30)
        response = self.client.get(reverse('articles:index'))
        self.assertQuerysetEqual(
            response.context['latest_article_list'],
            ['<Article: Past article.>']
        )

    def test_future_article(self):
        """
        Articles with a pub_date in the future aren't displayed on
        the index page.
        """
        create_article(article_text="Future article.", days=30)
        response = self.client.get(reverse('articles:index'))
        self.assertContains(response, "No articles are available.")
        self.assertQuerysetEqual(response.context['latest_article_list'], [])

    def test_future_article_and_past_article(self):
        """
        Even if both past and future articles exist, only past articles
        are displayed.
        """
        create_article(article_text="Past article.", days=-30)
        create_article(article_text="Future article.", days=30)
        response = self.client.get(reverse('articles:index'))
        self.assertQuerysetEqual(
            response.context['latest_article_list'],
            ['<Article: Past article.>']
        )

    def test_two_past_articles(self):
        """
        The articles index page may display multiple articles.
        """
        create_article(article_text="Past article 1.", days=-30)
        create_article(article_text="Past article 2.", days=-5)
        response = self.client.get(reverse('articles:index'))
        self.assertQuerysetEqual(
            response.context['latest_article_list'],
            ['<Article: Past article 2.>', '<Article: Past article 1.>']
        )


class ArticleModelTests(TestCase):

    def test_was_published_recently_with_future_article(self):
        """
        was_published_recently() returns False for articles whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_article = Article(pub_date=time)
        self.assertIs(future_article.was_published_recently(), False)


def test_was_published_recently_with_old_article(self):
    """
    was_published_recently() returns False for articles whose pub_date
    is older than 1 day.
    """
    time = timezone.now() - datetime.timedelta(days=1, seconds=1)
    old_article = Article(pub_date=time)
    self.assertIs(old_article.was_published_recently(), False)


def test_was_published_recently_with_recent_article(self):
    """
    was_published_recently() returns True for articles whose pub_date
    is within the last day.
    """
    time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    recent_article = Article(pub_date=time)
    self.assertIs(recent_article.was_published_recently(), True)
